import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def load_pickle_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        exit(1)

def save_table_as_image(df, title):
    """
    Render a pandas table as an image with better spacing and save the image.
    """
    import textwrap
    def wrap_text(text, width=15):
        return "\n".join(textwrap.wrap(str(text), width=width))
    
    # Wrap column headers
    wrapped_col_labels = [wrap_text(col, width=20) for col in df.columns]

    # Adjust figure size according to number of rows
    fig, ax = plt.subplots(figsize=(18, 1.5 + len(df)*0.7))
    ax.axis('off')

    table = ax.table(
        cellText=df.values,
        colLabels=wrapped_col_labels,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.27, 3.5)  # Adjust scaling to improve readability

    plt.title(title, fontsize=14, pad=8)
    plt.savefig(f"Evaluation/evaluation_table/{title.replace(' ', '_')}_with_acc.png", bbox_inches='tight', dpi=300)
    print(f"Saved: {title.replace(' ', '_')}_with_acc.png")
    plt.close()

def generate_evaluation_table(true_matrix, eval_files, model_names, category):
    """
    Compute average precision, recall, and F1 score for each model in a given category.
    Then, build a table and export it as an image.
    """
    table_data = []
    num_images = true_matrix.shape[0]
    
    for idx, file in enumerate(eval_files):
        # Load and reshape predicted matrix, ensuring shape matches the true matrix
        pred_matrix = np.nan_to_num(np.array(load_pickle_file(file)).reshape(true_matrix.shape), nan=0)
        precision_scores = []
        recall_scores = []
        f1_scores = []
        accuracy_scores = []
        
        # Calculate metrics for each image (row)
        for i in range(num_images):
            precision = precision_score(true_matrix[i], pred_matrix[i], average='macro', zero_division=0)
            recall = recall_score(true_matrix[i], pred_matrix[i], average='macro', zero_division=0)
            f1 = f1_score(true_matrix[i], pred_matrix[i], average='macro', zero_division=0)
            accuracy = accuracy_score(true_matrix[i], pred_matrix[i])

            precision_scores.append(precision)
            recall_scores.append(recall)
            f1_scores.append(f1)
            accuracy_scores.append(accuracy)
        
        # Compute average scores across all images
        avg_precision = np.mean(precision_scores)
        avg_recall = np.mean(recall_scores)
        avg_f1 = np.mean(f1_scores)
        avg_accuracy = np.mean(accuracy_scores)
        
        table_data.append([model_names[idx],
                           round(avg_precision, 4),
                           round(avg_recall, 4),
                           round(avg_f1, 4),
                           round(avg_accuracy, 4)])
    
    # Create a DataFrame with the evaluation metrics
    df = pd.DataFrame(table_data, columns=["Model", "Precision", "Recall", "F1 Score", "Accuracy"])
    
    print(f"\n{category.upper()} CATEGORY EVALUATION TABLE:\n")
    print(df.to_string(index=False))
    print("-" * 60)
    
    save_table_as_image(df, f"{category} Evaluation Metrics")

if __name__ == "__main__":
    # Load the true label matrices for each category and reshape to 1000x10
    action_true = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Action_self_label.pkl')).reshape(1000, 10), nan=0)
    emotion_true = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Emotion_self_label.pkl')).reshape(1000, 10), nan=0)
    
    # Evaluation files for each category
    action_eval_files = ["vLLMs_mat/GPT_Actions.pkl","vLLMs_mat/FLorence_action.pkl","vLLMs_mat/LLaVa1.5_action.pkl"]
    emotion_eval_files = ["vLLMs_mat/GPT_Emotions.pkl","vLLMs_mat/Florence_emotion.pkl","vLLMs_mat/LLaVa1.5_emotion.pkl"]
    
    # Model names corresponding to the evaluation files
    model_names = ["GPT4o", "Florence t2", "LLaVa-1.5"]
    
    # Generate and export evaluation tables for each category
    generate_evaluation_table(action_true, action_eval_files, model_names, "Action")
    generate_evaluation_table(emotion_true, emotion_eval_files, model_names, "Emotion")
