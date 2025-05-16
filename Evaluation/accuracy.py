import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt

def load_pickle_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        exit(1)

actions = [
    "Operating heavy machinery",
    "Lifting and carrying materials",
    "Measuring and marking surfaces",
    "Mixing cement or concrete",
    "Collaborating in teams",
    "Using hand tools (e.g., hammering, drilling)",
    "Inspecting completed work",
    "Communicating with supervisors",
    "Following safety protocols",
    "Taking breaks/resting"
]

emotions = [
    "Focused",
    "Determined",
    "Tired",
    "Alert",
    "Satisfied",
    "Anxious",
    "Proud",
    "Frustrated",
    "Cooperative",
    "Relieved"
]

# Load the matrices
action_self_matrix = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Action_self_label.pkl')).reshape(1000, 10), nan=0)
emotion_self_matrix = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Emotion_self_label.pkl')).reshape(1000, 10), nan=0)

action_eval_files = ["vLLMs_mat/GPT_Actions.pkl","vLLMs_mat/FLorence_action.pkl","vLLMs_mat/LLaVa1.5_action.pkl"]
emotion_eval_files = ["vLLMs_mat/GPT_Emotions.pkl","vLLMs_mat/Florence_emotion.pkl","vLLMs_mat/LLaVa1.5_emotion.pkl"]

action_eval = []
emotion_eval = []

def unpickle(pred, arr):
    for file in arr:
        pred.append(np.nan_to_num(np.array(load_pickle_file(file)).reshape(1000, 10), nan=0))

unpickle(action_eval, action_eval_files)
unpickle(emotion_eval, emotion_eval_files)

def wrap_text(text, width=15):
    """Insert line breaks to wrap long text"""
    import textwrap
    return "\n".join(textwrap.wrap(text, width))

def save_table_as_image(df, category):
    """Render a pandas table as an image with better spacing and larger cells"""
    import textwrap

    def wrap_text(text, width=15):
        return "\n".join(textwrap.wrap(str(text), width=width))

    # Wrap column headers
    wrapped_col_labels = [wrap_text(col, width=20) for col in df.columns]

    # Adjust figure size: wider + taller for larger cells
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
    table.scale(1.27, 3.5)  # Make cells wider and taller

    # Reduce title padding to bring it closer to the table
    plt.title(f"{category} Category - Per-Class Accuracy by Model", fontsize=14, pad=8)

    plt.savefig(f"Evaluation/evaluation_table/{category}_accuracy_summary.png", bbox_inches='tight', dpi=300)
    print(f"Saved: {category}_accuracy_summary.png")
    plt.close()



def generate_accuracy_table(true_matrix, pred_matrices, model_names, category, class_descriptions):
    """Generate and export a 4x11 table (Model x Per-Class Accuracy) for one category"""
    table_data = []

    for i, pred in enumerate(pred_matrices):
        row = [model_names[i]]
        for j in range(10):
            TP = np.sum((true_matrix[:, j] == 1) & (pred[:, j] == 1))
            TN = np.sum((true_matrix[:, j] == 0) & (pred[:, j] == 0))
            total = len(true_matrix)
            accuracy = (TP + TN) / total
            row.append(round(accuracy, 4))
        table_data.append(row)

    # Create DataFrame
    col_labels = ["Model"] + class_descriptions
    df_table = pd.DataFrame(table_data, columns=col_labels)

    # Print for confirmation
    print(f"\n{category.upper()} CATEGORY ACCURACY TABLE:\n")
    print(df_table.to_string(index=False))
    print("-" * 60)

    # Plot and save as image
    save_table_as_image(df_table, category)

if __name__ == "__main__":
    model_names = ["GPT4o", "Florence t2", "LLaVa-1.5"]

    generate_accuracy_table(action_self_matrix, action_eval, model_names, "Action", actions)
    generate_accuracy_table(emotion_self_matrix, emotion_eval, model_names, "Emotion", emotions)


