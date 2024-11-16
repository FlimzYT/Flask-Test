from flask import Flask, render_template, request
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Draw
from time import sleep

app = Flask(__name__)
app.config['IMAGE_FOLDER'] = 'static/images'

img_path = "./images/drawing.png"

def get_smiles_from_iupac(iupac_name):
    
    try:
        compounds = pcp.get_compounds(iupac_name, 'name')
        if compounds:
            return compounds[0].isomeric_smiles
        else:
            print(f"No compound found for the IUPAC name '{iupac_name}'.")
            return None
        
    except Exception as e:
        print(f"Error retrieving SMILES for '{iupac_name}': {e}")
        return None
    
def draw_molecule_from_smiles(smiles):

    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            img = Draw.MolToImage(mol, size=(400, 400))
            img.save("./static/images/drawing.png")
            return(img_path)
        else:
            print("Unable to interpret SMILES string.")

    except Exception as e:
        print(f"Error with molecule: {e}")

def draw_molecule_from_iupac(iupac_name):

    smiles = get_smiles_from_iupac(iupac_name)
    if smiles:
        print(f"Generating molecular diagram for '{iupac_name}'")
        sleep(3.0)
        return draw_molecule_from_smiles(smiles)
    else:
        print("Unable to draw molecule.")


def draw(num1, num2, operation):
    try:
        num1, num2 = float(num1), float(num2)
        if operation == '+':
            return round(num1 + num2, 2)
        elif operation == '-':
            return round(num1 - num2, 2)
        elif operation == '*':
            return round(num1 * num2, 2)
        elif operation == '/':
            if num2 == 0:
                return "Error: Division by zero"
            return round(num1 / num2, 2)
    except ValueError:
        return "Error: Invalid input"

@app.route('/', methods=['GET', 'POST'])
def start():
    result = ""
    if request.method == 'POST':
        name = request.form.get('name', '')
        result = draw_molecule_from_iupac(name)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)