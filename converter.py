import tkinter as tk
from tkinter import scrolledtext
import re
import xml.etree.ElementTree as ET


def convert_latex_integral_to_mathml_math(latex_string):
    # Define a mapping for LaTeX to MathML conversion
    latex_to_mathml = {
        r'\int': '<mo>&#x222B;</mo>',
        r'dx': '<mi>d</mi><mi>x</mi>',
        r'd': '<mi>d</mi>',
        r'(': '<mo>(</mo>',
        r')': '<mo>)</mo>',
        r'f': '<mi>f</mi>',
        r'x': '<mi>x</mi>',
    }
    
    # Replace LaTeX symbols with MathML equivalents
    for symbol, replacement in latex_to_mathml.items():
        latex_string = latex_string.replace(symbol, replacement)
    
    # Wrap the expression in MathML tags
    mathml_integral = f'<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>{latex_string}</mrow></math>'
    
    return mathml_integral

def convert_mathml_integral_to_latex_math(mathml):
    # Define a mapping for MathML to LaTeX conversion
    mathml_to_latex = {
        "{http://www.w3.org/1998/Math/MathML}mo": {
            "&#x222B;": r"\int",
        },
        "{http://www.w3.org/1998/Math/MathML}mi": {
            "d": r"d",
        },
    }

    # Function to recursively convert MathML to LaTeX
    def mathml_to_latex_recursive(element):
        if element.tag in mathml_to_latex:
            text = mathml_to_latex[element.tag].get(element.text, element.text)
            return text
        else:
            return "".join(mathml_to_latex_recursive(child) for child in element)

    # Convert MathML to LaTeX
    latex_integral = mathml_to_latex_recursive(ET.fromstring(mathml))

    return latex_integral

def convert_latex_derivative_to_mathml_math(latex_string):
    # Define a mapping for LaTeX to MathML conversion
    latex_to_mathml = {
        r'\frac{d}{dx}': '<mrow><mo>&#x2202;</mo><mrow><mi>d</mi></mrow><mo>/</mo><mrow><mi>dx</mi></mrow></mrow>',
    }
    
    # Replace LaTeX symbols with MathML equivalents
    for symbol, replacement in latex_to_mathml.items():
        latex_string = latex_string.replace(symbol, replacement)
    
    # Wrap the expression in MathML tags
    mathml_derivative = f'<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow>{latex_string}</mrow></math>'
    
    return mathml_derivative





def convert_mathml_derivative_to_latex_math(mathml):
    # Regular expression to match MathML derivatives
    pattern = r"<mrow><mo>&#x2202;</mo><mrow><mi>(.*?)</mi></mrow><mo>&#x2215;</mo><mrow><mo>&#x2202;</mo><mrow><mi>(.*?)</mi></mrow></mrow></mrow><msup><mi>(.*?)</mi><mn>(.*?)</mn></msup><mn>(.*?)</mn></mrow>"

    match = re.search(pattern, mathml)
    
    if match:
        derivative_variable, denominator_variable, base_expression, order, constant = match.groups()
        if constant:
            constant = f"{constant} "
        else:
            constant = ""
        
        latex_derivative = f"\\frac{{d^{order}}}{{d{derivative_variable}^{order}}}({constant}{base_expression})"
        return latex_derivative
    else:
        return "Error: Invalid MathML derivative"

# Example usage:
mathml_input = "<mrow><mo>&#x2202;</mo><mrow><mi>(x)</mi></mrow><mo>&#x2215;</mo><mrow><mo>&#x2202;</mo><mrow><mi>(y)</mi></mrow></mrow></mrow><msup><mi>(f)</mi><mn>(2)</mn></msup><mn>(5)</mn></mrow>"
latex_output = convert_mathml_derivative_to_latex_math(mathml_input)
print(latex_output)


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MathML and LaTeX Converter")
        self.root.configure(bg='light blue')

        self.create_ui()
        self.mathml_derivative_label = tk.Label(root, text="MathML Derivative:")
        self.mathml_derivative_label.grid(row=5, column=0, padx=5, pady=5)

        self.mathml_derivative_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=4)
        self.mathml_derivative_text.grid(row=5, column=1, padx=5, pady=5)

        self.convert_derivative_button = tk.Button(root, text="Convert to LaTeX (Derivative)", command=self.convert_mathml_derivative_to_latex, bg='light blue')
        self.convert_derivative_button.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

        self.latex_derivative_label = tk.Label(root, text="LaTeX Derivative:")
        self.latex_derivative_label.grid(row=6, column=0, padx=5, pady=5)

        self.latex_derivative_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=4)
        self.latex_derivative_text.grid(row=6, column=1, padx=5, pady=5)

        self.convert_latex_derivative_button = tk.Button(root, text="Convert to MathML (Derivative)", command=self.convert_latex_derivative_to_mathml, bg='light blue')
        self.convert_latex_derivative_button.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

        self.latex_integral_label = tk.Label(root, text="LaTeX Integral:")
        self.latex_integral_label.grid(row=7, column=0, padx=5, pady=5)

        self.latex_integral_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=4)
        self.latex_integral_text.grid(row=7, column=1, padx=5, pady=5)

        self.convert_latex_integral_button = tk.Button(root, text="Convert to MathML Integral", command=self.convert_latex_integral_to_mathml, bg='light blue')
        self.convert_latex_integral_button.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

        self.mathml_integral_label = tk.Label(root, text="MathML Integral:")
        self.mathml_integral_label.grid(row=8, column=0, padx=5, pady=5)

        self.mathml_integral_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=4)
        self.mathml_integral_text.grid(row=8, column=1, padx=5, pady=5)

        self.convert_mathml_integral_button = tk.Button(root, text="Convert to LaTeX Integral", command=self.convert_mathml_integral_to_latex, bg='light blue')
        self.convert_mathml_integral_button.grid(row=8, column=2, columnspan=2, padx=5, pady=5)

    def create_ui(self):
        self.create_latex_to_mathml_section()
        self.create_mathml_to_latex_section()


    def convert_mathml_integral_to_latex(self):
        mathml_input = self.mathml_integral_text.get("1.0", tk.END).strip()
        try:
            latex_output = convert_mathml_integral_to_latex_math(mathml_input)
            self.latex_integral_text.delete("1.0", tk.END)
            self.latex_integral_text.insert(tk.END, latex_output)
        except Exception as e:
            self.latex_integral_text.delete("1.0", tk.END)
            self.latex_integral_text.insert(tk.END, f"Error: {e}")

    def convert_latex_integral_to_mathml(self):
        latex_input = self.latex_integral_text.get("1.0", tk.END).strip()
        try:
            mathml_output = convert_latex_integral_to_mathml_math(latex_input)
            self.latex_integral_text.delete("1.0", tk.END)
            self.mathml_integral_text.insert(tk.END, mathml_output)
        except Exception as e:
            self.latex_integral_text.delete("1.0", tk.END)
            self.mathml_integral_text.insert(tk.END, f"Error: {e}")

    def convert_mathml_derivative_to_latex(self):
        mathml_input = self.mathml_derivative_text.get("1.0", tk.END).strip()
        try:
            latex_output = convert_mathml_derivative_to_latex_math(mathml_input)
            self.latex_derivative_text.delete("1.0", tk.END)
            self.latex_derivative_text.insert(tk.END, latex_output)
        except Exception as e:
            self.latex_derivative_text.delete("1.0", tk.END)
            self.latex_derivative_text.insert(tk.END, f"Error: {e}")

    def convert_latex_derivative_to_mathml(self):
        latex_input = self.latex_derivative_text.get("1.0", tk.END).strip()
        try:
            mathml_output = convert_latex_derivative_to_mathml_math(latex_input)
            self.mathml_derivative_text.delete("1.0", tk.END)
            self.mathml_derivative_text.insert(tk.END, mathml_output)
        except Exception as e:
            self.mathml_derivative_text.delete("1.0", tk.END)
            self.mathml_derivative_text.insert(tk.END, f"Error: {e}")

    def create_latex_to_mathml_section(self):
        latex_label = tk.Label(self.root, text="LaTeX:")
        latex_label.grid(row=0, column=0, padx=5, pady=5)

        self.latex_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=5)
        self.latex_text.grid(row=0, column=1, padx=5, pady=5)

        convert_button = tk.Button(self.root, text="Convert to MathML", command=self.convert_to_mathml, bg='light blue')
        convert_button.grid(row=0, column=2, padx=5, pady=5)

        latex_matrix_label = tk.Label(self.root, text="LaTeX Matrix:")
        latex_matrix_label.grid(row=1, column=0, padx=5, pady=5)

        self.latex_matrix_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=5)
        self.latex_matrix_text.grid(row=1, column=1, padx=5, pady=5)

        convert_matrix_button = tk.Button(self.root, text="Convert to MathML (Matrix)", command=self.convert_to_mathml_matrix, bg='light blue')
        convert_matrix_button.grid(row=1, column=2, padx=5, pady=5)

    def convert_to_latex_matrix(self):
        mathml_input = self.mathml_matrix_text.get("1.0", tk.END).strip()
        try:
            latex_output = self.convert_mathml_matrix_to_latex(mathml_input)
            self.latex_matrix_text.delete("1.0", tk.END)
            self.latex_matrix_text.insert(tk.END, latex_output)
        except Exception as e:
            self.latex_matrix_text.delete("1.0", tk.END)
            self.latex_matrix_text.insert(tk.END, f"Error: {e}")

    def create_mathml_to_latex_section(self):
        mathml_label = tk.Label(self.root, text="MathML:")
        mathml_label.grid(row=3, column=0, padx=5, pady=5)

        self.mathml_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=5)
        self.mathml_text.grid(row=3, column=1, padx=5, pady=5)

        convert_button = tk.Button(self.root, text="Convert to LaTeX", command=self.convert_to_latex, bg='light blue')
        convert_button.grid(row=3, column=2, padx=5, pady=5)

        mathml_matrix_label = tk.Label(self.root, text="MathML Matrix:")
        mathml_matrix_label.grid(row=4, column=0, padx=5, pady=5)

        self.mathml_matrix_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=5)
        self.mathml_matrix_text.grid(row=4, column=1, padx=5, pady=5)

        convert_matrix_button = tk.Button(self.root, text="Convert to LaTeX (Matrix)", command=self.convert_to_latex_matrix, bg='light blue')
        convert_matrix_button.grid(row=4, column=2, padx=5, pady=5)

    def convert_to_mathml(self):
        latex_input = self.latex_text.get("1.0", tk.END).strip()
        try:
            mathml_output = self.convert_latex_to_mathml(latex_input)
            self.mathml_text.delete("1.0", tk.END)
            self.mathml_text.insert(tk.END, mathml_output)
        except Exception as e:
            self.mathml_text.delete("1.0", tk.END)
            self.mathml_text.insert(tk.END, f"Error: {e}")

    def convert_latex_to_mathml(self, latex):
        mathml = "<math><mrow>"
        stack = []

        i = 0
        while i < len(latex):
            char = latex[i]

            if char.isalpha():
                term = char
                i += 1
                while i < len(latex) and latex[i].isalpha():
                    term += latex[i]
                    i += 1
                mathml += "<mi>{}</mi>".format(term)
            elif char.isdigit():
                coefficient = char
                i += 1
                while i < len(latex) and latex[i].isdigit():
                    coefficient += latex[i]
                    i += 1
                mathml += "<mn>{}</mn>".format(coefficient)
            elif char in "+-*/":
                mathml += "<mo>{}</mo>".format(char)
                i += 1
            elif char == "^":
                mathml += "<msup>"
                i += 1
            elif char == "(":
                stack.append(mathml)
                mathml = "<mrow>"
                i += 1
            elif char == ")":
                subexpression = mathml + "</mrow>"
                mathml = stack.pop() + subexpression
                i += 1
            else:
                i += 1

        mathml += "</mrow></math>"
        return mathml

    def convert_to_mathml_matrix(self):
        latex_input = self.latex_matrix_text.get("1.0", tk.END).strip()
        try:
            mathml_output = self.convert_latex_matrix_to_mathml(latex_input)
            self.mathml_matrix_text.delete("1.0", tk.END)
            self.mathml_matrix_text.insert(tk.END, mathml_output)
        except Exception as e:
            self.mathml_matrix_text.delete("1.0", tk.END)
            self.mathml_matrix_text.insert(tk.END, f"Error: {e}")

    def convert_latex_matrix_to_mathml(self, latex):
        latex = latex.strip()
        latex = latex.replace(r"\begin{bmatrix}", "").replace(r"\end{bmatrix}", "")
        rows = latex.split(r"\\")
        mathml = "<math><mrow><mo>[</mo>"

        for row in rows:
            elements = row.strip().split("&")
            mathml += "<mrow>"
            for element in elements:
                mathml += "<mtd><mi>{}</mi></mtd>".format(element.strip())
            mathml += "</mrow>"

        mathml += "<mo>]</mo></mrow></math>"
        return mathml

    def convert_mathml_matrix_to_latex(self, mathml):
        matrix_start = mathml.index("<mo>[</mo>") + len("<mo>[</mo>")
        matrix_end = mathml.rindex("<mo>]</mo>")

        matrix_content = mathml[matrix_start:matrix_end]
        rows = matrix_content.split("<mrow>")

        latex = "\\begin{bmatrix}"

        for row in rows[1:]:
            columns = row.split("<mtd>")
            elements = [col.replace("</mtd>", "").replace("<mi>", "").replace("</mi>", "").replace("<mn>", "").replace("</mn>", "").strip() for col in columns[1:] if col.strip()]
            end_string = ""
            if(len(elements) > 0):
                end_string = r" \\ "
            latex += " & ".join(elements) + end_string

        latex += "\\end{bmatrix}"
        latex = latex.replace("</mrow>", "")  # Remove any trailing </mrow> tag
        return latex

    def convert_to_latex(self):
        mathml_input = self.mathml_text.get("1.0", tk.END).strip()
        try:
            latex_output = self.convert_mathml_to_latex(mathml_input)
            self.latex_text.delete("1.0", tk.END)
            self.latex_text.insert(tk.END, latex_output)
        except Exception as e:
            self.latex_text.delete("1.0", tk.END)
            self.latex_text.insert(tk.END, f"Error: {e}")

    def convert_subexpression_to_latex(self, subexpression):
        # Function to convert subexpression (e.g., a + (b + c))
        latex = subexpression.replace("<mrow>", "(").replace("</mrow>", ")")
        latex = latex.replace("<mi>", "").replace("</mi>", "").replace("<mo>", "").replace("</mo>", "")
        latex = latex.replace("<msup>", "^{").replace("</msup>", "}")
        latex = latex.replace("<msub>", "_{").replace("</msub>", "")
        latex = latex.replace("<mfrac>", "{").replace("</mfrac>", "}")
        return latex

    def convert_mathml_to_latex(self, mathml):
        latex = mathml.replace("<math><mrow>", "").replace("</mrow></math>", "").replace("<mi>", "").replace("</mi>", "").replace("<mo>", "").replace("</mo>", "")
        latex = latex.replace("<mn>", "").replace("</mn>", "").replace("<msup>", "^{").replace("</msup>", "}")
        latex = latex.replace("<msub>", "_{").replace("</msub>", "").replace("<mfrac>", "{").replace("</mfrac>", "}")
        return latex

    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = ConverterApp(root)
    app.run()

if __name__ == "__main__":
    main()
