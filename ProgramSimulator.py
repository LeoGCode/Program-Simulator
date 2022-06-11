# Implementation of a simulator of programs, interpreters and translators based on Tombstone diagrams
# (a) It's able to handle programs, interpreters and translators. These can be:
# - PROGRAM <name> <language>.
# Represents a program identified by <name> written in <language>.
# - INTERPRETER <base_language> <language>
# Represents an interpreter for <language> written in <base_language>.
# - TRANSLATOR <base_language> <source_language> <target_language>.
# Represents a translator, from <origin_language> to <target_language>, written in <base_language>.
# (b) All languages must be alphanumeric strings.
# (c) There shall be a special name LOCAL which shall refer to the language that can be interpreted by the local
# machine. the local machine can interpret.
# (d) Once the program has started, it will repeatedly prompt the user for an action to proceed. Such action may be:
#
# i. DEFINE <type> [<arguments>].
# Represents a class definition <type> with <arguments> (see above for the types and arguments to be supported).
# The program should report an error and ignore the action if <name> already has an associated program, in the
# case of programs.
#
# ii. EXECUTABLE <name>
# Represents a query for the possibility of executing the program of name <name>. Your program must print whether
# it is possible to construct what is requested, using only the definitions made so far. The program should report an
# error and ignore the action if <name> does not have an
# associated program.
#
# iii. EXIT
# You must exit the simulator.
#
# At the end of the execution of each action, the program shall prompt the user for the next action.
# to the user.

import networkx as nx
import matplotlib.pyplot as plt


class ProgramSimulator:
    def __init__(self):
        language_graph = nx.DiGraph()
        language_graph.add_node("LOCAL")
        self.language_graph = language_graph
        self.programs = []
        self.language_programs = []
        self.translators = []

    def begin_program(self):
        print("Welcome to the program simulator!")

        # Main loop of the interactive program
        while True:
            action = input("Enter an action: ")
            param = action.split(" ")
            first_param = param.pop(0).upper()
            if first_param == "DEFINE" or first_param == "1" or first_param == "DEFINIR":
                # Verify the number of parameters
                if len(param) != 4 and len(param) != 3:
                    print("Error: Invalid number of parameters")
                    continue
                self.define(param)

            elif first_param == "EXECUTABLE" or first_param == "2" or first_param == "EXECUTABLE":
                # Verify the number of parameters
                if len(param) != 1:
                    print("Error: Invalid number of parameters")
                    continue
                self.executable(param)

            elif first_param == "EXIT" or first_param == "3" or first_param == "SALIR":
                break

            elif first_param == "DISPLAY" or first_param == "4" or first_param == "MOSTRAR":
                # Display the graph
                nx.draw_circular(self.language_graph, with_labels=True, arrowsize=25, font_size=8, node_size=1200)
                plt.axis('equal')
                plt.show()

            else:
                print("Error: Invalid action")

    def define(self, param):
        # Get the graph
        language_graph = self.language_graph

        # Verify the option
        option_type = param[0].upper()
        if option_type == "PROGRAM" or option_type == "1" or option_type == "PROGRAMA":
            # Verify the parameters
            if self.verify_program_param(param):
                name = param[1]
                language = param[2]

                self.programs.append(name)
                self.language_programs.append(language)
                if not language_graph.has_node(language):
                    language_graph.add_node(language)
                print("Was defined the program '" + name + "', executable in '" + language + "'")

        elif option_type == "INTERPRETER" or option_type == "2" or option_type == "INTERPRETE":
            # Verify the parameters
            if self.verify_interpreter_param(param):
                base_language = param[1]
                language = param[2]

                self.interpreter(base_language, language)

        elif option_type == "TRANSLATOR" or option_type == "3" or option_type == "TRADUCTOR":
            # Verify the parameters
            if self.verify_translator_param(param):
                base_language = param[1]
                source_language = param[2]
                target_language = param[3]

                self.translator(base_language, source_language, target_language)

        else:
            print("Error: Invalid type")
            return

    def interpreter(self, base_language, language):
        language_graph = self.language_graph
        # Verify if the language is already defined
        if not language_graph.has_node(base_language):
            language_graph.add_node(language)

        if not language_graph.has_node(language):
            language_graph.add_node(language)

        # Add edge from base_language to language
        if not language_graph.has_edge(language, base_language):
            self.language_graph.add_edge(language, base_language)
            # Update the translators to know if it can be added the interpreter associated to the translator
            self.update_translators()

        print("Was defined a interpreter for '" + language + "', written in '" + base_language + "'")

    def translator(self,base_language, source_language, target_language):
        language_graph = self.language_graph
        # If the language is not in the graph, its added
        if not language_graph.has_node(base_language):
            language_graph.add_node(base_language)

        if not language_graph.has_node(source_language):
            language_graph.add_node(source_language)

        if not language_graph.has_node(target_language):
            language_graph.add_node(target_language)

        # If exists a path from base language to LOCAL, its added the edge
        # from source language to target language
        if nx.has_path(language_graph, base_language, "LOCAL"):
            language_graph.add_edge(source_language, target_language)

            # We update the translators searching if a new interpreter can be added
            self.update_translators()
        else:
            # If not, we add the translator to the list and track if we can add the interpreter
            # associated to the translator in the moment of add a interpreter
            self.translators.append(Translator(base_language, source_language, target_language))

        print("Was defined a translator from '" + source_language + "' to ""'" + target_language +
              "', written in '" + base_language + "'")

    def verify_program_param(self, param):
        # Verify enough parameters
        if len(param) != 3:
            print("Error: Invalid number of parameters")
            return False

        name = param[1]
        language = param[2]

        # Verify if the program already exists
        if name in self.programs:
            print("Error: Program already defined")
            return False

        # Verify language is alphanumeric
        if not language.isalnum():
            print("Error: the language must be alphanumeric")
            return False

        return True

    @staticmethod
    def verify_interpreter_param(param):
        # Verify enough parameters
        if len(param) != 3:
            print("Error: Invalid number of parameters")
            return False

        base_language = param[1]
        language = param[2]

        # Verify languages are alphanumeric
        if not base_language.isalnum() or not language.isalnum():
            print("Error: the all languages must be alphanumeric")
            return False

        return True

    @staticmethod
    def verify_translator_param(param):
        # Verify enough parameters
        if len(param) != 4:
            print("Error: Invalid number of parameters")
            return False

        base_language = param[1]
        source_language = param[2]
        target_language = param[3]

        # Verify languages are alphanumeric
        if not base_language.isalnum() or not source_language.isalnum() or not target_language.isalnum():
            print("Error: the all languages must be alphanumeric")
            return False

        return True

    def executable(self, param):

        name: str = param[0]
        # Verify if the program already exists
        if name not in self.programs:
            print("Error: Program not defined")
            return

        index_name = self.programs.index(name)
        language = self.language_programs[index_name]
        language_graph = self.language_graph
        # We search the path from the language of the program to the local language
        # if exists, the program can be executed, otherwise, it can't
        if nx.has_path(language_graph, language, "LOCAL"):
            print("Yes, is posible to execute the program " + name)
        else:
            print("No, is not possible to execute the program " + name)

    def update_translators(self):
        # We traverse the list of translators searching if the interpreter associated to the translator can be added
        for translator in self.translators:
            # If the interpreter can be added, we add it and we update the list of translators again
            if nx.has_path(self.language_graph, translator.base_language, "LOCAL"):
                self.language_graph.add_edge(translator.source_language, translator.target_language)
                # We remove the translator from the list, because his interpreter was added
                # and it is no longer necessary to track him
                self.translators.remove(translator)
                self.update_translators()


class Translator:
    def __init__(self, base_language, source_language, target_language):
        self.base_language = base_language
        self.source_language = source_language
        self.target_language = target_language
