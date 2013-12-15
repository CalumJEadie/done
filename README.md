done
====

A graphical interface for your todo.txt file.

Usage
-----

```sh
git clone git@github.com:CalumJEadie/done.git
cd done
./done.sh
```

Dependancies
------------

[PySide](http://qt-project.org/wiki/Get-PySide) - Python Qt bindings


Motivation
----------

I'm a huge fan of Gina Trapani's [todo.txt](http://todotxt.com/) method for managing a todo list. I've often thought about what the GUI equivalent of the speed of a todo.txt file would be. So, a few evenings ago I put some [mock ups together](http://www.calumjeadie.com/2013/12/01/what-would-a-really-optimised-GUI-for-Todo.txt-look-like%3F.html) and this evening thought I'd see how far I could get in a couple of hours.

Features
--------

- Use a text editor to edit your todo.txt file, rather than the indirection of the command line client or row based GUI clients.
- Instant update. Any changes in the editor are written to disk straight away. If you're storing your todo.txt file in a service like Dropbox, it'll sync straight away, like in the Todo.txt Android App.
- Sort by due date.