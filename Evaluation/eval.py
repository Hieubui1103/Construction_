import pickle
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

# Load the pickle files with debug info
try:
    with open('vLLMs_mat/Action_self_label.pkl', 'rb') as f:
        action_self_matrix = pickle.load(f)
        print("Successfully loaded Action_self_label.pkl")
except FileNotFoundError:
    print("Error: Action_self_label.pkl not found")
    exit(1)

action_self_matrix = np.array(action_self_matrix).reshape(1000, 10)
action_self_matrix = np.nan_to_num(action_self_matrix, nan=0)

try:
    with open('vLLMs_mat/Emotion_self_label.pkl', 'rb') as f:
        Emotion_self_matrix = pickle.load(f)
        print("Successfully loaded Emotion_self_label.pkl")
except FileNotFoundError:
    print("Error: Emotion_self_label.pkl not found")
    exit(1)

Emotion_self_matrix = np.array(Emotion_self_matrix).reshape(1000, 10)
Emotion_self_matrix = np.nan_to_num(Emotion_self_matrix, nan=0)

action_eval = ["vLLMs_mat/GPT_Actions.pkl","vLLMs_mat/FLorence_action.pkl","vLLMs_mat/LLaVa1.5_action.pkl"]
Emotion_eval = ["vLLMs_mat/GPT_Emotions.pkl","vLLMs_mat/Florence_emotion.pkl","vLLMs_mat/LLaVa1.5_emotion.pkl"]

def evaluation(eval_type, eval_truth, mode):
    data_act_dict = {}
    matrix_act_dict = {}
    # Calculate metrics for each row (1000 rows total)
    precision_scores = []
    recall_scores = []
    f1_scores = []

    # action evaluation
    for act_file in eval_type:
        try:
            with open(act_file, 'rb') as f:
                data_act_dict[act_file] = pickle.load(f)
                print(f"\nSuccessfully loaded {act_file} ")
        except FileNotFoundError:
            print("Error: file not found")
            exit(1)

        # Ensure matrices are numpy arrays and have the correct shape (1000x10)
        matrix_act_dict[act_file] = np.array(data_act_dict[act_file]).reshape(1000, 10)

        for i in range(1000):
            # Calculate metrics for each row with zero_division handling
            precision = precision_score(eval_truth[i], matrix_act_dict[act_file][i], average='macro', zero_division=0)
            recall = recall_score(eval_truth[i], matrix_act_dict[act_file][i], average='macro', zero_division=0)
            f1 = f1_score(eval_truth[i], matrix_act_dict[act_file][i], average='macro', zero_division=0)

            
            precision_scores.append(precision)
            recall_scores.append(recall)
            f1_scores.append(f1)
        
        # Calculate average scores across all rows
        avg_precision = np.mean(precision_scores)
        avg_recall = np.mean(recall_scores)
        avg_f1 = np.mean(f1_scores)

        # Print results
        print(f"\nAverage statistics for 1000 images overall for {mode} in {act_file} to hand-craft self-label:")
        print(f"Average Precision: {avg_precision:.4f}")
        print(f"Average Recall: {avg_recall:.4f}")
        print(f"Average F1 Score: {avg_f1:.4f}")

evaluation(action_eval,action_self_matrix, "actions")
evaluation(Emotion_eval,Emotion_self_matrix, "emotions")
                    