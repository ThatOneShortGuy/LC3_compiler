# With this compiler, will come a custom language as well.
We are still deciding how we want this language to work, and are open to suggestions.
The end goal is to make it for the LC-3.
Pehaps, we may even make it work for other systems as well.

Some considered language options:
- Typdef (like in C)
- Functional
- Easy to write (like python)
<b> Both `;` and `\n` as statement separators
<b> Both `\t` and `{...}` as block separators
- For variable of type `char`, do the operation on the ascii value (`char c = 'a'` c + 1 would be 'b')
- Arrays of numbers would work like `int arr[3] = 1, 2, 3; arr++;` and arr would be `[2, 3, 4]`