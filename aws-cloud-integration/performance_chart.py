import matplotlib.pyplot as plt

# Dummy model accuracy values (example data)
epochs = [1, 2, 3, 4, 5]
accuracy = [72, 78, 83, 87, 91]

plt.figure(figsize=(8,5))
plt.plot(epochs, accuracy, marker='o', linewidth=2)
plt.title("AI Model Performance Over Training Iterations")
plt.xlabel("Epochs")
plt.ylabel("Accuracy (%)")
plt.grid(True)
plt.tight_layout()

# Save chart
plt.savefig("screenshots/performance.png")
print("✅ Performance chart saved successfully in screenshots/performance.png")
