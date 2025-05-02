
# Comments

- Submission: P2_jensnorr
- Final score: 22/30
- Date: 2024-10-20 13:32:20

## General comments
You need to check the input/output lecture and notebook for how to use `with open()` to read files. Great that you added the `add_force` method. Also great that you added the `move` method, however it does more than `moving`, it also resets the forces to 0, consider adding a new method called `reset_forces`.

## E1 : Read file into graph
This function does not work as intended on a mac.
This line
```python
    edgevalues = nonbinary_text.split("\r\n")
```
works on mac if:
```python
    edgevalues = nonbinary_text.split("\n")
```
Please see the input/output lecture and notebook for how to use `with open()` to read files, this function should look like:
```python
    with open(filename, "r") as data:
        nodes = int(data.readline())
        for line in data:
            edge = tuple(map(int, line.split()))
            edges.append(edge)
``` 

## E2 : Initialize initial locations
Nice and clean. Consider using `enumerate` to get the index and node, could make the code more readable.

## E3 : Implement repel
Nice job. Great use of the `add_force` method. Only minor comments is you do not need to put `-1 *` in front of the force, you can just do `-f_rep * np.cos(angle)`.

## E4 : Implement attract
similar as above.

## E5 : Implement update
Good work on the combination logic, however it could be made more readable by using two for loops, e.g.:

```python
    for i, node1 in enumerate(self.nodes):
        for node2 in self.nodes[i+1:]:
            node1.repel(node2)
```

Please also note the use of meaningful names, `item` does not tell me anything about what it is, `node1` and `node2` do. Otherwise, good use of the `move` method.

## E6 : Add max iterations argument
Good work with the argument, however your simulation does not stop at the expected `max_iterations`. And inside the `run` function, you are looping over the range of `max_iterations` again. I was surprised how fast the simulation converged, but realised it was running 100 times per step :-)
