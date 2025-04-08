import argparse
import os
import re
import subprocess

from graphviz import Digraph


def parse_dig_file(file_path):
    """
    Parse a .dig file to extract task dependencies.
    Returns a list of tuples representing dependencies (task, dependency).
    """
    dependencies = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Match task definitions and their dependencies
            match = re.search(r'(require>):\s*([^\s]+)', line)
            if match:
                dependency = match.group(2)
                dependencies.append((os.path.basename(file_path).replace('.dig', ''), dependency))
    return dependencies

def create_dependency_graph(folder_path, output_file):
    """
    Create a dependency graph for all .dig files in the folder.
    """
    graph = Digraph(format='png')
    graph.attr(rankdir='TB')  # Top-to-bottom layout
    graph.attr('node', shape='box', style='filled', color='lightblue')

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.dig'):
            file_path = os.path.join(folder_path, file_name)
            print(f"Parsing file: {file_name}")
            dependencies = parse_dig_file(file_path)
            print(f"Dependencies found: {dependencies}")
            for task, dep in dependencies:
                edge_color = 'blue' if 'call>' in dep else 'green'
                graph.edge(dep, task.replace('.dig', ''), color=edge_color)

    graph.render(output_file, cleanup=True)
    print(f"Graph rendering complete. Output file: {output_file}.png")
    print(f"Dependency graph saved as {output_file}.png")

    # Open the generated image
    subprocess.run(["open", f"{output_file}.png"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a dependency graph for .dig files.")
    parser.add_argument("--folder_path", type=str, help="Path to the folder containing .dig files")
    parser.add_argument("--output_file", type=str, help="Name of the output file (without extension)")
    args = parser.parse_args()

    create_dependency_graph(args.folder_path, args.output_file)
