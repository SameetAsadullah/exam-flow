# Genetic algorithm design

The timetable is represented as a chromosome with one gene per course. Each exam gene contains a day, time slot, one or more rooms, and an invigilator for each room.

## Search cycle

1. Load courses, students, registrations, and teachers from the CSV datasets.
2. Generate an initial population of random timetables.
3. Score every chromosome by counting scheduling conflicts.
4. Select candidates using roulette-wheel selection.
5. Create new candidates through crossover and mutation.
6. Repeat until the stopping condition is reached, then display the fittest timetable.

## Constraints represented in fitness

- A student cannot sit two exams in the same slot.
- A room cannot host two exams simultaneously.
- An invigilator cannot supervise overlapping exams.
- Invigilator scheduling should avoid consecutive assignments.
- Management courses should precede computer-science courses where applicable.

The original project statement and report provide the full academic specification and evaluation.
