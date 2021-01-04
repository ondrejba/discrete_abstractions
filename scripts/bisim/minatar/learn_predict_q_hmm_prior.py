import argparse
import os
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D         # don't delete this, necessary for 3d projection
import constants
from utils.logger import LearnExpectationContinuousLogger
from utils.saver import Saver
from runners.bisim.minatar.QHMMPrior import QHMMPriorRunnerMinAtar

SAVE_PREFIX = "{:s}/minatar/q_hmm_predictor_bisim_v1"
SAVE_TEMPLATE = "{:s}_{:s}_{:d}_blocks_{:d}_components_{:g}_beta0" \
                "_{:g}_beta1_{:g}_beta2_{:g}_beta3_{:g}_elr_{:s}_opt_{:d}_steps"
BATCH_SIZE = 100


def main(args):

    np.random.seed(2019)

    if not args.show_graphs:
        matplotlib.use("pdf")

    if args.gpus is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpus

    saver = Saver(None)

    if args.save:
        dir_variables = [
            SAVE_PREFIX.format(args.base_dir), args.game, args.num_blocks, args.num_components,
            args.beta0, args.beta1, args.beta2, args.beta3, args.encoder_learning_rate, args.encoder_optimizer,
            args.num_steps
        ]
        dir_switches = [
            "no_sample", "only_one_q_value", "disable_batch_norm", "train_prior",
            "post_train_prior", "post_train_t_and_prior", "post_train_hmm"
        ]

        saver.create_dir_name(SAVE_TEMPLATE, dir_variables, dir_switches, args)
        saver.create_dir(add_run_subdir=True)

    saver.save_by_print(args, "settings")

    logger = LearnExpectationContinuousLogger(save_file=saver.get_save_file("main", "log"), print_logs=True)
    logger.silence_tensorflow()

    num_actions = 6

    model_learning_rate = args.encoder_learning_rate
    if args.model_learning_rate is not None:
        model_learning_rate = args.model_learning_rate

    runner = QHMMPriorRunnerMinAtar(
        args.load_path, args.game, num_actions, logger, saver, args.num_blocks, args.num_components,
        args.encoder_learning_rate, args.beta0, args.beta1, args.beta2, args.weight_decay,
        args.encoder_optimizer, args.num_steps, disable_batch_norm=args.disable_batch_norm,
        disable_softplus=args.disable_softplus, no_sample=args.no_sample, only_one_q_value=args.only_one_q_value,
        validation_freq=args.validation_freq, validation_fraction=args.validation_fraction, summaries=args.summaries,
        load_model_path=args.load_model_path, beta3=args.beta3, post_train_prior=args.post_train_prior,
        post_train_hmm=args.post_train_hmm, post_train_t_and_prior=args.post_train_t_and_prior,
        save_gifs=args.save_gifs, zero_sd_after_training=args.zero_sd_after_training,
        hard_abstract_state=args.hard_abstract_state, freeze_hmm_no_entropy_at=args.freeze_hmm_no_entropy_at,
        cluster_predict_qs=args.cluster_predict_qs, cluster_predict_qs_weight=args.cluster_predict_qs_weight,
        prune_threshold=args.prune_threshold, prune_abstraction=args.prune_abstraction,
        prune_abstraction_new_means=args.prune_abstraction_new_means, sample_abstract_state=args.sample_abstract_state,
        softmax_policy=args.softmax_policy, softmax_policy_temp=args.softmax_policy_temp,
        discount=args.discount, fix_prior_training=args.fix_prior_training,
        model_learning_rate=model_learning_rate, q_scaling_factor=args.q_scaling_factor,
        eval_episodes=args.eval_episodes
    )

    runner.setup()
    runner.main_training_loop()

    if args.post_train_hmm:
        runner.post_hmm_training_loop(args.post_train_hmm_steps)

    if args.save_model:
        runner.save_model()

    runner.evaluate_and_visualize()
    runner.close_model_session()


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Learn to predict q-values with an HMM prior in MinAtar games.")

    parser.add_argument("load_path", help="dataset load path")
    parser.add_argument("game", help="game")

    parser.add_argument("--num-blocks", type=int, default=32, help="continuous latent space size")
    parser.add_argument("--num-components", type=int, default=500, help="discrete latent space size")
    parser.add_argument("--validation-fraction", type=float, default=0.2, help="validation fraction of the dataset")
    parser.add_argument("--validation-freq", type=int, default=1000, help="validation frequency")
    parser.add_argument("--oversample", default=False, action="store_true", help="oversample rewards>0")
    parser.add_argument("--disable-softplus", default=False, action="store_true",
                        help="do not use softplus on samples sds")
    parser.add_argument("--beta0", type=float, default=1.0, help="q loss weight")
    parser.add_argument("--beta1", type=float, default=0.0001, help="entropy loss weight")
    parser.add_argument("--beta2", type=float, default=0.0001, help="prior loss weight")
    parser.add_argument("--beta3", type=float, default=0.0, help="don't touch this")
    parser.add_argument("--no-sample", default=False, action="store_true", help="do not sample from encoder Gaussian")
    parser.add_argument("--only-one-q-value", default=False, action="store_true", help="use only one q-value")
    parser.add_argument("--train-prior", default=False, action="store_true", help="train prior on prior")
    parser.add_argument("--post-train-prior", default=False, action="store_true",
                        help="train prior on prior after training")
    parser.add_argument("--post-train-t-and-prior", default=False, action="store_true",
                        help="train T and prior on prior after training")
    parser.add_argument("--post-train-hmm", default=False, action="store_true",
                        help="train the whole HMM after training")
    parser.add_argument("--post-train-hmm-steps", type=int, default=1000, help="number of steps")
    parser.add_argument("--zero-sd-after-training", default=False, action="store_true",
                        help="zero encoder sd after training")
    parser.add_argument("--hard-abstract-state", default=False, action="store_true",
                        help="take argmax of the probabilities over the current discrete abstract state")
    parser.add_argument("--freeze-hmm-no-entropy-at", default=None, type=int)
    parser.add_argument("--cluster-predict-qs", default=False, action="store_true",
                        help="predict q-values from abstract states")
    parser.add_argument("--cluster-predict-qs-weight", type=float, default=0.1,
                        help="loss weight")
    parser.add_argument("--prune-abstraction", default=False, action="store_true", help="prune state abstraction")
    parser.add_argument("--prune-threshold", type=float, default=0.01,
                        help="prune state abstraction threshold on number of samples")
    parser.add_argument("--prune-abstraction-new-means", default=False, action="store_true",
                        help="another pruning method")
    parser.add_argument("--sample-abstract-state", default=False, action="store_true", help="sample abstract states")
    parser.add_argument("--softmax-policy", default=False, action="store_true", help="abstract softmax policy")
    parser.add_argument("--softmax-policy-temp", type=float, default=1.0, help="abstract softmax policy temperature")
    parser.add_argument("--discount", type=float, default=0.9, help="discount factor")
    parser.add_argument("--q-scaling-factor", type=float, default=10.0, help="scaling factor for q-values")
    parser.add_argument("--eval-episodes", type=int, default=100, help="number of evaluation episodes")

    parser.add_argument("--encoder-learning-rate", type=float, default=0.001, help="encoder learning rate")
    parser.add_argument("--model-learning-rate", type=float, default=None, help="model learning rate")
    parser.add_argument("--fix-prior-training", default=False, action="store_true", help="fix loss weights")
    parser.add_argument("--weight-decay", type=float, default=0.0001, help="weight decay")
    parser.add_argument("--encoder-optimizer",
                        help=", ".join([constants.OPT_ADAM, constants.OPT_MOMENTUM, constants.OPT_SGD]),
                        default=constants.OPT_ADAM)
    parser.add_argument("--num-steps", type=int, default=50000, help="number of training steps")
    parser.add_argument("--disable-batch-norm", default=False, action="store_true", help="disable batch norm")

    parser.add_argument("--save", default=False, action="store_true", help="save results")
    parser.add_argument("--base-dir", default="results", help="base save dir")
    parser.add_argument("--show-graphs", default=False, action="store_true", help="show graphs")
    parser.add_argument("--save-gifs", default=False, action="store_true", help="show abstract agent episodes")
    parser.add_argument("--summaries", default=False, action="store_true", help="save tf summaries")
    parser.add_argument("--save-model", default=False, action="store_true", help="save model weights")
    parser.add_argument("--load-model-path", help="load model path")
    parser.add_argument("--gpus", help="comma-separated list of gpus to use")

    parsed = parser.parse_args()
    main(parsed)
