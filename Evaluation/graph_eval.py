import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def load_pickle_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        exit(1)

def evaluate_models(eval_files, ground_truth):
    results = {}
    
    for file in eval_files:
        model_name = file.split('/')[-1].split('.')[0]  # Extract model name from filename
        pred_matrix = np.array(load_pickle_file(file)).reshape(1000, 10)
        
        precision_scores = []
        recall_scores = []
        f1_scores = []
        accuracy_scores = []
        
        for i in range(1000):
            precision = precision_score(ground_truth[i], pred_matrix[i], average='macro', zero_division=0)
            recall = recall_score(ground_truth[i], pred_matrix[i], average='macro', zero_division=0)
            f1 = f1_score(ground_truth[i], pred_matrix[i], average='macro', zero_division=0)
            accuracy = accuracy_score(ground_truth[i], pred_matrix[i])

            precision_scores.append(precision)
            recall_scores.append(recall)
            f1_scores.append(f1)
            accuracy_scores.append(accuracy)
        
        results[model_name] = {
            'precision': np.mean(precision_scores),
            'recall': np.mean(recall_scores),
            'f1': np.mean(f1_scores),
            'accuracy': np.mean(accuracy_scores)
        }
    
    return results

def plot_metrics(results, category):
    metrics = ['precision', 'recall', 'f1', 'accuracy']
    models = list(results.keys())
    values = {metric: [results[model][metric] for model in models] for metric in metrics}
    
    x = np.arange(len(models))  # Label locations
    width = 0.2  # Bar width
    
    fig, ax = plt.subplots()
    for i, metric in enumerate(metrics):
        ax.bar(x + i * width, values[metric], width, label=metric)
    
    ax.set_xlabel('Models')
    ax.set_ylabel('Scores')
    ax.set_title(f'Model Performance Comparison ({category})')
    ax.set_xticks(x + width)
    ax.set_xticklabels(models, rotation = 0)
    ax.legend()
    
    plt.savefig(f"Evaluation/evaluation_table/{category}_comparison_with_acc.png", bbox_inches='tight', dpi=300)

# Load ground truth matrices
action_self_matrix = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Action_self_label.pkl')).reshape(1000, 10), nan=0)
Emotion_self_matrix = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Emotion_self_label.pkl')).reshape(1000, 10), nan=0)

action_eval_files = ["vLLMs_mat/GPT_Actions.pkl","vLLMs_mat/FLorence_action.pkl","vLLMs_mat/LLaVa1.5_action.pkl"]
emotion_eval_files = ["vLLMs_mat/GPT_Emotions.pkl","vLLMs_mat/Florence_emotion.pkl","vLLMs_mat/LLaVa1.5_emotion.pkl"]
# Evaluate models
action_results = evaluate_models(action_eval_files, action_self_matrix)
emotion_results = evaluate_models(emotion_eval_files, Emotion_self_matrix)

# Plot results
plot_metrics(action_results, "Actions")
plot_metrics(emotion_results, "Emotions")
