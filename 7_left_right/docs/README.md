# Nonogram - Solution

The MIP formulation of the puzzle is documented in PDF and as a jupyter notebook. 
However, because of some math expressions, the jupyter notebook may not get rendered properly 
depending on where you are trying open it.

- [nonogram_formulation.pdf](nonogram_formulation.pdf)
- [nonogram_formulation.ipynb](left_right_formulation.ipynb).

**Solution:**

Here is one possible solution (there are multiple solutions to this puzzle).  
```python
[1, 1, 1, 1, 0, 1, 0, 1, 1, 0]
[0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
[1, 0, 0, 0, 1, 1, 1, 0, 1, 1]
[0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
[0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
[1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 1, 1, 1]
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0]
[0, 1, 0, 1, 1, 1, 1, 0, 1, 1]
[0, 0, 0, 0, 0, 1, 1, 0, 1, 1]
```
![Nonogram solution](nonogram_solution.png)

Back to the [main page](../../README.md).