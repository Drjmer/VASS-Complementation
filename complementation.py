from collections import deque

class PetriNet:
    def __init__(self, places, transitions, arcs, labeling):
        self.places = places  # Set of places
        self.transitions = transitions  # Set of transitions
        self.arcs = arcs  # Mapping (transition) -> vector change
        self.labeling = labeling  # Mapping transition -> label

    #Fires a transition if enabled, returning the new marking.
    def fire_transition(self, marking, transition):
        if not self.is_enabled(marking, transition):
            return None  # Transition not enabled
        
        new_marking = tuple(m + v for m, v in zip(marking, self.arcs[transition]))
        return new_marking

    #Checks if a transition is enabled at a given marking.
    def is_enabled(self, marking, transition):
        return all(m + v >= 0 for m, v in zip(marking, self.arcs[transition]))

    #Constructs the reachability graph from the initial marking.
    def reachability_graph(self, initial_marking):
        queue = deque([initial_marking])
        visited = set()
        transitions_fired = {}


        #using breadth first search to reach each and every reachable node
        while queue:
            marking = queue.popleft()
            if marking in visited:
                continue
            visited.add(marking)

            for transition in self.transitions:
                if self.is_enabled(marking, transition):
                    new_marking = self.fire_transition(marking, transition)
                    if new_marking and new_marking not in visited:
                        queue.append(new_marking)
                        transitions_fired[(marking, transition)] = new_marking

        return visited, transitions_fired

    #Computes the complement Petri net N' with proper final markings.
    def compute_complement(self, initial_marking, upward_closure):
        reachable, _ = self.reachability_graph(initial_marking)

        # Complement states: states NOT reaching the upward closure
        complement_states = {marking for marking in reachable if not any(
            all(m >= f for m, f in zip(marking, forbidden)) for forbidden in [upward_closure]
        )}

        print(f"Complement States: {complement_states}") 
        
        # Compute final markings (f') in the complement Petri net
        final_markings = set()
        for marking in complement_states:
            if all(self.fire_transition(marking, t) in complement_states or self.fire_transition(marking, t) is None
                   for t in self.transitions):
                final_markings.add(marking)

        # Construct N' as the complement of N
        new_places = self.places
        new_transitions = self.transitions
        new_arcs = self.arcs
        new_labeling = self.labeling

        new_initial_marking = initial_marking
        new_final_marking = final_markings  # The newly computed final markings

        return PetriNet(new_places, new_transitions, new_arcs, new_labeling), new_initial_marking, new_final_marking


# === EXAMPLE TEST CASE ===
places = {"s", "p1", "p2", "q1", "q2"}
transitions = {"t1", "t2", "t3", "t4"}
arcs = {
    "t1": (-1, 1, 0, 0, 0),  # s -> p1 (a)
    "t2": (0, -1, 1, 0, 0),  # p1 -> p2 (b)
    "t3": (-1, 0, 0, 1, 0),  # s -> q1 (b)
    "t4": (0, 0, 0, -1, 1)   # q1 -> q2 (a)
}
labeling = {"t1": "a", "t2": "b", "t3": "b", "t4": "a"}

petri_net = PetriNet(places, transitions, arcs, labeling)
initial_marking = (1, 0, 0, 0, 0)  # Start in s
upward_closure = (0, 0, 1, 0, 1)  # Upward closure of final markings

N_prime, s_prime, f_prime = petri_net.compute_complement(initial_marking, upward_closure)

print("Initial Marking:", s_prime)
print("Final Markings:", f_prime)
