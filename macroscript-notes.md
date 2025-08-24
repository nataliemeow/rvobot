# MacroScript notes

MacroScript is the high-level macro language used by RIC. it's somewhat similar to [Tcl](https://en.wikipedia.org/wiki/Tcl) if you've ever heard of that.

here's how you write Hello World:

```
Hello World
```

(yup)

## language

MS is a very simple language. (whether it is *easy* is debatable.) the 4 primary constructs in MacroScript (in my categorization anyway) are:

- **strings:** just strings.
- **function calls:** of the form `[name/argument/...]`.
- **escaped strings:** strings with all `[`, `/`, `]` and `\` characters prefixed with `\`. this causes MacroScript to not evaluate these until they are unescaped.
- **unescapes:** of the form `[unescape/str]`. causes an escaped string to be evaluated on demand. actually a built-in function but it's significant enough for me to consider as something different.

execution is done in steps by repeatedly replacing function calls with their output; from left to right, from inner to outer-most.

### a simple example

```
[store/x/1][add/[load/x]/1]
```

`store` is a built-in function that sets a variable and returns nothing (i.e. an empty string). next:

```
[add/[load/x]/1]
```

`load` returns the content of a variable. next:

```
[add/1/1]
```

lastly, the final output is:

```
2
```

### loops

to do anything more complex like loops and branches, you need escaping and unescaping. to demonstrate, here's an example that prints squares from 1 to 100:

```
[store/i/1][unescape/[repeat/10/\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]]]
```

output:

```
1.0 4.0 9.0 16.0 25.0 36.0 49.0 64.0 81.0 100.0 
```

---

in the first step, the working string becomes:

```
[unescape/[repeat/10/\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]]]
```

with the variable `i` set to `1`.

in the next step, this happens:

```
[unescape/\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]\[multiply\/\[load\/i\]\/\[load\/i\]\] \[store\/i\/\[add\/\[load\/i\]\/1\]\]]
```

notice how the loop isn't being evaluated yet because it was escaped with backslashes. to evaluate it, we apply `unescape`:

```
[multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]][multiply/[load/i]/[load/i]] [store/i/[add/[load/i]/1]]
```

and from there:

```
1.0 4.0 9.0 16.0 25.0 36.0 49.0 64.0 81.0 100.0 
```

## MSW

MSW is my attempt to improve MacroScript syntax. in MSW, the example from earlier would look like:

```clj
(set i 1)
,(repeat 10 (* .i .i) '[
	.i " "
	(set i (+ .i 1))
])
```

naturally this isn't much better since it has the same weird semantics, but it makes code way easier to read and write in my experience.