#!/usr/bin/env bash


beta=0.000001

for i in {0..9} ; do

    python -m scripts.bisim.puck_stack.learn_predict_q_hmm_prior_multi_task dataset/4x4_dqn_2_pucks_1_r_eps_0.1_rs.pickle 4 3 \
    --active-indices 0 --eval-indices 1 2 3 4 5 6 7 --dones-index 0 \
     --num-blocks 32 --num-components 1000 --encoder-learning-rate 0.001 --model-learning-rate 0.01 \
    --beta0 1 --beta1 $beta --beta2 $beta --goal-rewards-threshold 0.99 --softmax-policy --softmax-policy-temp 0.01 \
    --encoder-optimizer adam --num-steps 50000 --fix-prior-training --post-train-hmm --post-train-hmm-steps 50000 \
    --gpus 0 --save --base-dir results/icml/4x4_dqn_2_pucks_1_r_eps_0.1_rs --random-shape

    python -m scripts.bisim.puck_stack.learn_predict_q_hmm_prior_multi_task dataset/4x4_dqn_3_pucks_eps_0.1_rs.pickle 4 3 \
    --active-indices 1 --eval-indices 0 2 3 4 5 6 7 --dones-index 1 \
    --num-blocks 32 --num-components 1000 --encoder-learning-rate 0.001 --model-learning-rate 0.01 \
    --beta0 1 --beta1 $beta --beta2 $beta --goal-rewards-threshold 0.99 --softmax-policy --softmax-policy-temp 0.01 \
    --encoder-optimizer adam --num-steps 50000 --fix-prior-training --post-train-hmm --post-train-hmm-steps 50000 \
    --gpus 0 --save --base-dir results/icml/4x4_dqn_3_pucks_eps_0.1_rs --random-shape

    python -m scripts.bisim.puck_stack.learn_predict_q_hmm_prior_multi_task dataset/4x4_dqn_3_stairs_eps_0.1_rs.pickle 4 3 \
    --active-indices 5 --eval-indices 0 1 2 3 4 6 7 --dones-index 5 \
    --num-blocks 32 --num-components 1000 --encoder-learning-rate 0.001 --model-learning-rate 0.01 \
    --beta0 1 --beta1 $beta --beta2 $beta --goal-rewards-threshold 0.99 --softmax-policy --softmax-policy-temp 0.01 \
    --encoder-optimizer adam --num-steps 50000 --fix-prior-training --post-train-hmm --post-train-hmm-steps 50000 \
    --gpus 0 --save --base-dir results/icml/4x4_dqn_3_stairs_eps_0.1_rs --random-shape

    python -m scripts.bisim.puck_stack.learn_predict_q_hmm_prior_multi_task dataset/4x4_dqn_3_pucks_and_3_row_eps_0.1_rs.pickle 4 3 \
    --active-indices 1 3 --eval-indices 0 2 4 5 6 7 --dones-index 1 \
    --num-blocks 32 --num-components 1000 --encoder-learning-rate 0.001 --model-learning-rate 0.01 \
    --beta0 1 --beta1 $beta --beta2 $beta --goal-rewards-threshold 0.99 --softmax-policy --softmax-policy-temp 0.01 \
    --encoder-optimizer adam --num-steps 50000 --fix-prior-training --post-train-hmm --post-train-hmm-steps 50000 \
    --gpus 0 --save --base-dir results/icml/4x4_dqn_3_pucks_and_3_row_eps_0.1_rs --random-shape

    python -m scripts.bisim.puck_stack.learn_predict_q_hmm_prior_multi_task dataset/4x4_dqn_3_pucks_and_3_stairs_eps_0.1_rs.pickle 4 3 \
    --active-indices 1 5 --eval-indices 0 2 3 4 6 7 --dones-index 1 \
    --num-blocks 32 --num-components 1000 --encoder-learning-rate 0.001 --model-learning-rate 0.01 \
    --beta0 1 --beta1 $beta --beta2 $beta --goal-rewards-threshold 0.99 --softmax-policy --softmax-policy-temp 0.01 \
    --encoder-optimizer adam --num-steps 50000 --fix-prior-training --post-train-hmm --post-train-hmm-steps 50000 \
    --gpus 0 --save --base-dir results/icml/4x4_dqn_3_pucks_and_3_stairs_eps_0.1_rs --random-shape

done
