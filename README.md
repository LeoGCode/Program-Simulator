# Program-Simulator
Implementation of a simulator of programs, interpreters and translators based on Tombstone diagrams

This program has the following characteristics:
* It's able to handle programs, interpreters and translators, these can be.
    - PROGRAM \<name> \<language>.
  
      Represents a program identified by \<name> written in \<language>.
    - INTERPRETER \<base_language> \<language>

      Represents an interpreter for \<language> written in <base_language>.
    - TRANSLATOR \<base_language> \<source_language> \<target_language>.
    
      Represents a translator, from \<origin_language> to \<target_language>, written in \<base_language>.
* All languages must be alphanumeric strings.
* There shall be a special name "LOCAL" which shall refer to the language that can be interpreted by the local
machine.
* Once the program has started, it will repeatedly prompt the user for an action to proceed. Such action may be:

    - DEFINE \<type> [\<arguments>].
    
      Represents a class definition \<type> with \<arguments> (see above for the types and arguments to be supported).
The program should report an error and ignore the action if \<name> already has an associated program, in the
case of programs.
  
    - EXECUTABLE \<name>
    
      Represents a query for the possibility of executing the program of name \<name>. Your program must print whether
it is possible to construct what is requested, using only the definitions made so far. The program should report an
error and ignore the action if <name> does not have an
associated program.
  
    - EXIT
  
      Exit the simulator.
    
    - DISPLAY
    
      Show the graph representation of the programs and his posibility to be execute on some language
  
At the end of the execution of each action, the program shall prompt to the user for the next action.
    
A digraph was used for the implementation of the model, where the nodes are the different languages defined and the edges are the possibility of executing some language based on another, when defining an interpreter a edge is added from the language that can be interpreted to the language in which it was written, in the case of translators, the side from the source language to the target language is only added if there is a path in the network from the base language to "LOCAL", for this reason when a translator is added it will be added to a list of translators that do not have such connection so that when adding a connection, this list will be searched to see if the translator can be updated. 
