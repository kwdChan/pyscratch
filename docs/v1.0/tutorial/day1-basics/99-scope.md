---
title: Extra - Variables Scope
parent: Day 1 - Basics
nav_order: 99
---

# Shared Variables
{: .no_toc }

---


{: .highlight-title }
> Key takeaway
> 1. **Variables only used within a function**: You can create it inside the function. 
>     - *In most cases, you cannot access the variables created inside a function from the outside.* 
> 2. **Variables used within a script**: You can create it outside the functions. 
>     - For example, the sprite objects (`player1` or `player2`) are typically created outside the functions.  
> 3. **Variables used across scripts**: You have to put it in side the `game` object. 


## Challenge
You need to know the scope of the variables very well. To test your understanding, see this example:

### Problem: *Predict* what will happen without running the script.

**Answer the following:**
- What lines will lead to errors? Remove these lines.  
- After the fix, what numbers will be printed out? 
- After the fix, in what sequence will the numbers be printed out? 

<details open markdown="block">
  <summary>
    Code
  </summary>

```python 
x = 10

def my_function1():
    x = 5
    y = 20
    print("x from my_function1: ", x)
    print("y from my_function1: ", y)

def my_function2():
    print("x from my_function2: ", x)
    print("y from my_function2: ", y) 
    
print("x from outside: ", x)
my_function1()
my_function2()
print("x from outside: ", x)
print("y from outside: ", y)
```
</details>

<details markdown="block">
  <summary>
    Answer
  </summary>

<details open markdown="block">
  <summary>
    The lines causing errors
  </summary>

```python 
print("y from my_function2: ", y) 
# and 
print("y from outside: ", y)
```
</details>
<details open markdown="block">
  <summary>
    Expected Output
  </summary>


```
x from outside: 10
x from my_function1: 5
y from my_function1: 20
x from my_function2: 10
x from outside: 10
```
</details>
</details>

If you get it right, great. Go to the next section. Otherwise, 
 see <a href="https://www.w3schools.com/python/python_scope.asp" target="_blank">this external tutorial </a>. 

