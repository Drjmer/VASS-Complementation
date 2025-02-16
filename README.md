# Complement Petri Net Computation

## Overview
This project implements a Petri net system and computes its complement. A Petri net is a mathematical modeling tool used for describing distributed systems. The goal of this implementation is to compute the complement of a given deterministic Petri net by identifying states that do not reach a specified upward closure set.

## Features
- Defines a Petri net with places, transitions, and labeled arcs.
- Simulates the firing of transitions to determine reachability.
- Constructs a reachability graph from an initial marking.
- Computes the complement of a given Petri net by finding states that do not reach the upward closure.
- Identifies the final markings in the complement Petri net.

## Installation
This implementation requires Python 3.x.

1. Clone the repository or copy the source code.
2. Ensure you have Python installed.
3. Run the script directly using:
   ```sh
   python complement_petri_net.py
   ```

## Usage
The script defines a `PetriNet` class with the following key methods:

- `fire_transition(marking, transition)`: Attempts to fire a transition and returns the new marking.
- `is_enabled(marking, transition)`: Checks if a transition can be fired given the current marking.
- `reachability_graph(initial_marking)`: Constructs the reachability graph starting from an initial marking.
- `compute_complement(initial_marking, upward_closure)`: Computes the complement Petri net, returning the new net and its updated markings.

### Example Usage
The script includes a sample Petri net:
```python
places = {"p0", "p1"}
transitions = {"t1", "t2"}
arcs = {
    "t1": (-1, 1, 0),  # Moves tokens from p0 to p1
    "t2": (0, -1, 1)   # Moves tokens from p1 back to p0
}
labeling = {"t1": "a", "t2": "b"}

petri_net = PetriNet(places, transitions, arcs, labeling)
initial_marking = (1, 0, 0)  # Start with 1 token in p0, 0 in p1
upward_closure = (0, 0, 1)  # Upward closure marking

N_prime, s_prime, f_prime = petri_net.compute_complement(initial_marking, upward_closure)

print("Complement Petri Net:")
print("Places:", N_prime.places)
print("Transitions:", N_prime.transitions)
print("Arcs:", N_prime.arcs)
print("Initial Marking:", s_prime)
print("Final Markings:", f_prime)
```

## Expected Output
This program computes the complement of the Petri net and prints the new places, transitions, arcs, initial marking, and final markings.

## Notes
- This implementation assumes a **deterministic** Petri net, meaning that for any reachable marking, each label corresponds to at most one enabled transition.
- The complement states are determined by identifying states that do not reach the upward closure.
- Final markings in the complement Petri net are those where no transitions lead out or all outgoing transitions remain within the complement states.