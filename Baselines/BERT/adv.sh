#CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run_leven.py \
#	--data_dir ./new_data \
#	--model_type bert \
#	--output_dir ./saved_20240311_no-adv \
#	--max_seq_length 512 \
#	--per_gpu_train_batch_size 15 \
#	--per_gpu_eval_batch_size 15 \
#	--gradient_accumulation_steps 1 \
#	--learning_rate 5e-5 \
#	--num_train_epochs 4 \
#	--save_steps 100 \
#	--seed 3407 \
#	--do_train \
#	--do_eval \
#	--eval_all_checkpoints \
#	--overwrite_output_dir \
#	--wandb leven_adv \
#	--wandbname no-adv
#
#CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run_leven.py \
#	--data_dir ./new_data \
#	--model_type bert \
#	--output_dir ./saved_20240311_fgm \
#	--max_seq_length 512 \
#	--per_gpu_train_batch_size 15 \
#	--per_gpu_eval_batch_size 15 \
#	--gradient_accumulation_steps 1 \
#	--learning_rate 5e-5 \
#	--num_train_epochs 4 \
#	--save_steps 100 \
#	--seed 3407 \
#	--do_train \
#	--do_eval \
#	--eval_all_checkpoints \
#	--overwrite_output_dir \
#	--wandb leven_adv \
#	--wandbname fgm \
#	--adv fgm

#CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run_leven.py \
#	--data_dir ./new_data \
#	--model_type bert \
#	--output_dir ./saved_20240311_FreeAT \
#	--max_seq_length 512 \
#	--per_gpu_train_batch_size 12 \
#	--per_gpu_eval_batch_size 12 \
#	--gradient_accumulation_steps 1 \
#	--learning_rate 5e-5 \
#	--num_train_epochs 4 \
#	--save_steps 100 \
#	--seed 3407 \
#	--do_train \
#	--do_eval \
#	--eval_all_checkpoints \
#	--overwrite_output_dir \
#	--wandb leven_adv \
#	--wandbname FreeAT \
#	--adv FreeAT
#
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run_leven.py \
	--data_dir ./new_data \
	--model_type bert \
	--output_dir ./saved_20240311_pgd \
	--max_seq_length 512 \
	--per_gpu_train_batch_size 12 \
	--per_gpu_eval_batch_size 12 \
	--gradient_accumulation_steps 1 \
	--learning_rate 5e-5 \
	--num_train_epochs 4 \
	--save_steps 100 \
	--seed 3407 \
	--do_train \
	--do_eval \
	--eval_all_checkpoints \
	--overwrite_output_dir \
	--wandb leven_adv \
	--wandbname pgd \
	--adv pgd

#CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run_leven.py \
#	--data_dir ./new_data \
#	--model_type bert \
#	--output_dir ./saved_20240311_fgsm \
#	--max_seq_length 512 \
#	--per_gpu_train_batch_size 15 \
#	--per_gpu_eval_batch_size 15 \
#	--gradient_accumulation_steps 1 \
#	--learning_rate 5e-5 \
#	--num_train_epochs 4 \
#	--save_steps 100 \
#	--seed 3407 \
#	--do_train \
#	--do_eval \
#	--eval_all_checkpoints \
#	--overwrite_output_dir \
#	--wandb leven_adv \
#	--wandbname fgsm \
#	--adv fgsm