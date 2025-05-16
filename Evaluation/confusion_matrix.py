import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Example: 1000x10 binary matrices (random data)
# np.random.seed(42)
# true = np.random.randint(0, 2, (1000, 10))  # Ground truth
# pred = np.random.randint(0, 2, (1000, 10))  # Model predictions

def load_pickle_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        exit(1)

action_self_matrix = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Action_self_label.pkl')).reshape(1000, 10), nan=0)
Emotion_self_matrix = np.nan_to_num(np.array(load_pickle_file('vLLMs_mat/Emotion_self_label.pkl')).reshape(1000, 10), nan=0)

action_eval_files = ["vLLMs_mat/GPT_Actions.pkl","vLLMs_mat/FLorence_action.pkl","vLLMs_mat/LLaVa1.5_action.pkl"]
emotion_eval_files = ["vLLMs_mat/GPT_Emotions.pkl","vLLMs_mat/Florence_emotion.pkl","vLLMs_mat/LLaVa1.5_emotion.pkl"]

action_eval = []
emtion_eval = []

def unpickle(pred, arr):
    for file in arr:
        pred.append(np.nan_to_num(np.array(load_pickle_file(file)).reshape(1000, 10), nan=0))

unpickle(action_eval, action_eval_files)
unpickle(emtion_eval, emotion_eval_files)

print(action_eval[0].shape)
print(emtion_eval[0].shape)
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
emotions = ["Focused",
            "Determined",
            "Tired",
            "Alert",
            "Satisfied",
            "Anxious",
            "Proud",
            "Frustrated",
            "Cooperative",
            "Relieved"]

def con_matrix(true, pred, name, category, class_arr):
    confusion_matrix = np.zeros((10, 10), dtype=int)

    for i in range(1000):
        true_labels = np.where(true[i] == 1)[0]
        pred_labels = np.where(pred[i] == 1)[0]

        for actual in true_labels:
            for predicted in pred_labels:
                confusion_matrix[actual, predicted] += 1
                
    class_labels = [f"Class {i+1}" for i in range(10)]
    df_confusion = pd.DataFrame(confusion_matrix, index=class_labels, columns=class_labels)

    plt.figure(figsize=(12, 8))
    sns.heatmap(df_confusion, annot=True, fmt="d", cmap="Blues", linewidths=0.5, cbar_kws={"shrink": 0.8})

    plt.title(f"Confusion Matrix of {name} for {category.capitalize()}", fontsize=14)
    plt.xlabel("Predicted Class", fontsize=12)
    plt.ylabel("Actual Class", fontsize=12)

    # Annotate class descriptions explicitly on the left side of the heatmap
    for idx, label in enumerate(class_arr):
        plt.text(-1.5, 0.5 + idx*0.5, f"Class {idx+1}: {label}", 
                 va='center', ha='right', fontsize=10, color='black')

    # plt.tight_layout(rect=[0.2, 0, 1, 1])  # Adjust layout to accommodate annotations on left
    plt.subplots_adjust(left=0.35, right=0.98, top=0.92, bottom=0.08)
    plt.savefig(f"confusion_matrix/confusion_matrix_{name}_{category}.png", dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    name = ["GPT4o", "Florence t2", "LLaVa-1.5"]
    for i in range (len(action_eval)):
        con_matrix(action_self_matrix, action_eval[i], name[i], "action", actions)
    for i in range (len(emtion_eval)):
        con_matrix(Emotion_self_matrix, emtion_eval[i], name[i], "emotion",emotions)