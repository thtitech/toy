import unittest
#import expr_parser
#from expr_parser import myeval
import rpn_parser
from rpn_parser import myeval

class exprTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        # test for simple operation +, -, *, /
        self.assertEqual(5, myeval("2+3"))
        self.assertEqual(3.5, myeval("1.25+2.25"))
        self.assertEqual(-1, myeval("1-2"))
        self.assertEqual(1, myeval("3-2"))
        self.assertEqual(15, myeval("5*3"))
        self.assertEqual(2.0, myeval("4/2"))
        self.assertEqual(2.5, myeval("5/2"))

    def test_normal(self):
        self.assertEqual(-4, myeval("1-2-3"))
        self.assertEqual(10, myeval("(2+3)*2"))
        self.assertEqual(2.0, myeval("(10-4)/(1+2)"))
        self.assertEqual(18.0, myeval("((10-2)/4)*((1+2)*3)"))
    
    """
    def test_exception(self):
        with self.assertRaises(expr_parser.IllegalExpressionException):
            myeval("((1+2)/3*5")
    """        

if __name__ == "__main__":
    unittest.main()
