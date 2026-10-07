import xml.etree.ElementTree as ET

from tutor.ingest.mathml import math_to_text

M = 'xmlns:m="http://www.w3.org/1998/Math/MathML"'


def convert(inner: str) -> str:
    return math_to_text(ET.fromstring(f"<m:math {M}>{inner}</m:math>"))


def test_subscript_and_operator():
    assert convert("<m:msub><m:mi>F</m:mi><m:mtext>net</m:mtext></m:msub><m:mo>=</m:mo><m:mn>0</m:mn>") == "F_net = 0"


def test_fraction_and_power():
    assert convert("<m:mfrac><m:mi>m</m:mi><m:msup><m:mi>s</m:mi><m:mn>2</m:mn></m:msup></m:mfrac>") == "m/(s^2)"


def test_vector_arrow():
    assert convert("<m:mover><m:mi>v</m:mi><m:mo>→</m:mo></m:mover>") == "v⃗"


def test_square_root():
    assert convert("<m:msqrt><m:mi>x</m:mi></m:msqrt>") == "sqrt(x)"
