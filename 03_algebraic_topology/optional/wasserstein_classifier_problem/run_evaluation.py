import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns
import importlib
import sys

# Import student code
import implementation_tasks as tasks

def generate_circle(n=100, noise=0.0):
    theta = np.linspace(0, 2*np.pi, n)
    x = np.cos(theta) + np.random.normal(0, noise, n)
    y = np.sin(theta) + np.random.normal(0, noise, n)
    return np.column_stack([x, y])

def generate_figure8(n=100, noise=0.0):
    theta = np.linspace(0, 2*np.pi, n//2)
    # Circle 1 (Radius 1) at (0, 1) -> bottom touches (0, 0)
    x1 = np.cos(theta) + np.random.normal(0, noise, n//2)
    y1 = np.sin(theta) + 1 + np.random.normal(0, noise, n//2)
    # Circle 2 (Radius 2) at (0, -2) -> top touches (0, 0)
    x2 = 2 * np.cos(theta) + np.random.normal(0, noise, n//2)
    y2 = 2 * np.sin(theta) - 2 + np.random.normal(0, noise, n//2)
    return np.vstack([np.column_stack([x1, y1]), np.column_stack([x2, y2])])

def generate_cluster(n=100, noise=0.0):
    # Noise effectively controls the spread of the cluster
    x = np.random.normal(0, 1.0 + noise, n)
    y = np.random.normal(0, 1.0 + noise, n)
    return np.column_stack([x, y])

def rotate_points(points, angle):
    c, s = np.cos(angle), np.sin(angle)
    R = np.array(((c, -s), (s, c)))
    return points.dot(R.T)

def run_ml_evaluation(progress_callback=None):
    print("Generating Clean Reference Shapes...")
    ref_circle = generate_circle(n=100, noise=0.0)
    ref_figure8 = generate_figure8(n=100, noise=0.0)
    ref_cluster = generate_cluster(n=100, noise=0.0)

    print("Computing Reference Diagrams...")
    # Using a fairly generous max_edge_length to ensure cycles form
    max_edge = 5.0 
    
    try:
        ref_diags = {
            "circle": tasks.compute_h1_diagram(ref_circle, max_edge),
            "figure8": tasks.compute_h1_diagram(ref_figure8, max_edge),
            "cluster": tasks.compute_h1_diagram(ref_cluster, max_edge)
        }
        
        for val in ref_diags.values():
            if val is None:
                print("Error: compute_h1_diagram returned None. Please implement it first!")
                return
    except Exception as e:
        print(f"Error while computing reference diagrams: {e}")
        return

    print("Generating Dataset (300 shapes, varying noise and rotation)...")
    dataset = []
    labels = []
    
    # Generate 100 of each
    for _ in range(100):
        # Random noise between 0.05 and 0.25 (more realistic for good classification)
        noise_level = np.random.uniform(0.05, 0.25)
        angle = np.random.uniform(0, 2*np.pi)
        
        c = rotate_points(generate_circle(noise=noise_level), angle)
        dataset.append(c)
        labels.append("circle")
        
        f8 = rotate_points(generate_figure8(noise=noise_level), angle)
        dataset.append(f8)
        labels.append("figure8")
        
        cl = rotate_points(generate_cluster(noise=noise_level), angle)
        dataset.append(cl)
        labels.append("cluster")

    print(f"Classifying {len(dataset)} shapes...")
    predicted = []
    
    total = len(dataset)
    for i, points in enumerate(dataset):
        if progress_callback:
            progress_callback(i, total)
        else:
            if i > 0 and i % 30 == 0:
                print(f"Processed {i}/{total}...")
        try:
            diag = tasks.compute_h1_diagram(points, max_edge)
            pred = tasks.classify_shape(diag, ref_diags)
            
            if pred is None:
                print("\nError: classify_shape returned None. Please implement it first!")
                return
                
            predicted.append(pred)
        except Exception as e:
            print(f"\nError during classification: {e}")
            return

    acc = accuracy_score(labels, predicted)
    print(f"\nClassification Complete! Accuracy: {acc * 100:.2f}%")

    cm = confusion_matrix(labels, predicted, labels=["circle", "figure8", "cluster"])
    return acc, cm, ["circle", "figure8", "cluster"]

if __name__ == "__main__":
    run_ml_evaluation()
