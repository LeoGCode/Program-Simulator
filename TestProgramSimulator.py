import unittest
from unittest import mock
from ProgramSimulator import ProgramSimulator
from ProgramSimulator import Translator
import networkx as nx


class MyTestCase(unittest.TestCase):
    def test_init(self):
        ps = ProgramSimulator()
        self.assertTrue(ps.language_graph.is_directed())
        self.assertTrue(ps.language_graph.has_node("LOCAL"))
        self.assertEqual(len(ps.programs), 0)
        self.assertEqual(len(ps.language_programs), 0)
        self.assertEqual(len(ps.translators), 0)

    def test_Translator_init(self):
        translator = Translator("base_language", "source_language", "target_language")
        self.assertEqual(translator.base_language, "base_language")
        self.assertEqual(translator.source_language, "source_language")
        self.assertEqual(translator.target_language, "target_language")

    def test_verify_translator_param(self):
        ps = ProgramSimulator()
        correct_param = ["TRANSLATOR", "baseLanguage", "sourceLanguage", "targetLanguage"]
        self.assertTrue(ps.verify_translator_param(correct_param))
        wrong_number_param = ["TRANSLATOR", "baseLanguage", "sourceLanguage", "targetLanguage", "wrongParam"]
        self.assertFalse(ps.verify_translator_param(wrong_number_param))
        wrong_language_param = ["TRANSLATOR", "special_symbols-#$&", "sourceLanguage", "targetLanguage"]
        self.assertFalse(ps.verify_translator_param(wrong_language_param))
        wrong_language_param2 = ["TRANSLATOR", "baseLanguage", "special_symbols-#$&", "targetLanguage"]
        self.assertFalse(ps.verify_translator_param(wrong_language_param2))
        wrong_language_param3 = ["TRANSLATOR", "baseLanguage", "sourceLanguage", "special_symbols-#$&"]
        self.assertFalse(ps.verify_translator_param(wrong_language_param3))

    def test_verify_interpreter_param(self):
        ps = ProgramSimulator()
        correct_param = ["INTERPRETER", "baseLanguage", "language"]
        self.assertTrue(ps.verify_interpreter_param(correct_param))
        wrong_number_param = ["INTERPRETER", "baseLanguage", "language", "wrong_param"]
        self.assertFalse(ps.verify_interpreter_param(wrong_number_param))
        wrong_language_param = ["INTERPRETER", "special_symbols-#$&", "language"]
        self.assertFalse(ps.verify_interpreter_param(wrong_language_param))
        wrong_language_param2 = ["INTERPRETER", "baseLanguage", "special_symbols-#$&"]
        self.assertFalse(ps.verify_interpreter_param(wrong_language_param2))

    def test_verify_program_param(self):
        ps = ProgramSimulator()
        correct_param = ["PROGRAM", "name_program", "language"]
        self.assertTrue(ps.verify_program_param(correct_param))
        wrong_number_param = ["PROGRAM", "name_program", "language", "wrong_param"]
        self.assertFalse(ps.verify_program_param(wrong_number_param))
        wrong_language_param = ["PROGRAM", "name_program", "special_symbols-#$&"]
        self.assertFalse(ps.verify_program_param(wrong_language_param))

        ps.define(["PROGRAM", "name_program", "language"])
        wrong_program_name = ["PROGRAM", "name_program", "language"]
        self.assertFalse(ps.verify_program_param(wrong_program_name))

    def test_translator(self):
        ps = ProgramSimulator()
        no_path_to_local = ["baseLanguage", "sourceLanguage", "targetLanguage"]
        ps.translator(no_path_to_local[0], no_path_to_local[1], no_path_to_local[2])
        self.assertEqual(len(ps.translators), 1)
        self.assertEqual(ps.translators[0].base_language, "baseLanguage")
        self.assertEqual(ps.translators[0].source_language, "sourceLanguage")
        self.assertEqual(ps.translators[0].target_language, "targetLanguage")

        self.assertTrue(ps.language_graph.has_node("sourceLanguage"))
        self.assertTrue(ps.language_graph.has_node("targetLanguage"))
        self.assertTrue(ps.language_graph.has_node("baseLanguage"))
        self.assertFalse(nx.has_path(ps.language_graph, "sourceLanguage", "targetLanguage"))

        path_to_local = ["LOCAL", "sourceLanguage2", "targetLanguage2"]
        ps.translator(path_to_local[0], path_to_local[1], path_to_local[2])
        self.assertEqual(len(ps.translators), 1)
        self.assertNotEqual(ps.translators[0].base_language, "LOCAL")
        self.assertNotEqual(ps.translators[0].source_language, "sourceLanguage2")
        self.assertNotEqual(ps.translators[0].target_language, "targetLanguage2")

        self.assertTrue(ps.language_graph.has_node("LOCAL"))
        self.assertTrue(ps.language_graph.has_node("sourceLanguage2"))
        self.assertTrue(ps.language_graph.has_node("targetLanguage2"))
        self.assertTrue(nx.has_path(ps.language_graph, "sourceLanguage2", "targetLanguage2"))

    def test_interpreter(self):
        ps = ProgramSimulator()
        param = ["baseLanguage", "language"]
        ps.interpreter(param[0], param[1])
        self.assertTrue(nx.has_path(ps.language_graph, "language", "baseLanguage"))
        self.assertTrue(ps.language_graph.has_node("language"))
        self.assertTrue(ps.language_graph.has_node("baseLanguage"))

        param = ["baseLanguage2", "language2"]
        ps.interpreter(param[0], param[1])
        self.assertTrue(nx.has_path(ps.language_graph, "language2", "baseLanguage2"))
        self.assertTrue(ps.language_graph.has_node("language2"))
        self.assertTrue(ps.language_graph.has_node("baseLanguage2"))

    def test_define(self):
        ps = ProgramSimulator()
        invalid_type = ["invalid_type", "name_program", "language"]
        ps.define(invalid_type)
        self.assertEqual(len(ps.programs), 0)
        self.assertEqual(len(ps.language_programs), 0)
        self.assertEqual(len(ps.translators), 0)

        param_program = ["PROGRAM", "name_program", "language"]
        ps.define(param_program)
        self.assertEqual(len(ps.programs), 1)
        self.assertEqual(len(ps.language_programs), 1)
        self.assertEqual(len(ps.translators), 0)

        param_translator = ["TRANSLATOR", "baseLanguage", "sourceLanguage", "targetLanguage"]
        ps.define(param_translator)
        self.assertEqual(len(ps.programs), 1)
        self.assertEqual(len(ps.language_programs), 1)
        self.assertEqual(len(ps.translators), 1)

        param_interpreter = ["INTERPRETER", "baseLanguage", "language"]
        ps.define(param_interpreter)
        self.assertEqual(len(ps.programs), 1)
        self.assertEqual(len(ps.language_programs), 1)
        self.assertEqual(len(ps.translators), 1)
        self.assertTrue(nx.has_path(ps.language_graph, "language", "baseLanguage"))
        self.assertTrue(ps.language_graph.has_node("language"))
        self.assertTrue(ps.language_graph.has_node("baseLanguage"))

    def test_begin_program(self):
        ps = ProgramSimulator()
        test_cases_wrong_input = ["invalid_type name_program", "DEFINE PROGRAM wrong number program",
                                  "EXECUTABLE name_program wrong_number_param", "EXIT"]

        with mock.patch('builtins.input', side_effect=test_cases_wrong_input):
            ps.begin_program()
            self.assertEqual(len(ps.programs), 0)
            self.assertEqual(len(ps.language_programs), 0)
            self.assertEqual(len(ps.translators), 0)
            self.assertTrue(len(ps.language_graph.nodes) == 1)
            self.assertTrue(len(ps.language_graph.edges) == 0)

        test_cases_correct_input = ["DEFINE PROGRAM name_program language", "EXECUTABLE name_program", "EXIT"]
        with mock.patch('builtins.input', side_effect=test_cases_correct_input):
            ps.begin_program()
            self.assertEqual(len(ps.programs), 1)
            self.assertEqual(len(ps.language_programs), 1)
            self.assertEqual(len(ps.translators), 0)
            self.assertTrue(len(ps.language_graph.nodes) == 2)
            self.assertTrue(len(ps.language_graph.edges) == 0)

    def test_executable(self):
        ps = ProgramSimulator()
        ps.define(["PROGRAM", "name_program", "language"])
        ps.define(["INTERPRETER", "LOCAL", "language"])
        ps.executable(["name_program"])
        self.assertEqual(len(ps.programs), 1)
        self.assertEqual(len(ps.language_programs), 1)
        self.assertEqual(len(ps.translators), 0)
        self.assertTrue(len(ps.language_graph.nodes) == 2)

        ps.executable("wrong_name_program")
        self.assertEqual(len(ps.programs), 1)
        self.assertEqual(len(ps.language_programs), 1)
        self.assertEqual(len(ps.translators), 0)
        self.assertTrue(len(ps.language_graph.nodes) == 2)

        ps.define(["PROGRAM", "name_program2", "language2"])
        ps.executable(["name_program2"])
        self.assertEqual(len(ps.programs), 2)
        self.assertEqual(len(ps.language_programs), 2)
        self.assertEqual(len(ps.translators), 0)
        self.assertTrue(len(ps.language_graph.nodes) == 3)


if __name__ == '__main__':
    unittest.main()
