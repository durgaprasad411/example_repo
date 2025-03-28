import streamlit as st
import base64
import io
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
# this is an example comment

load_dotenv()
model=ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')



def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')  # Encode to Base64

st.title('Get the code solution here!!')
que=st.file_uploader('Upload the images of Question',type=["jpg", "jpeg", "png"],
        accept_multiple_files=True)
samples=st.file_uploader('Upload the images of sample input and output',type=["jpg", "jpeg", "png"],
        accept_multiple_files=True)
console=st.file_uploader('Upload the images of the console',type=["jpg", "jpeg", "png"],
        accept_multiple_files=True)
if (que or samples or console) and st.button('Get Code'):
    que_base64 = [encode_image(Image.open(img)) for img in que] if que else []
    sample_base64 = [encode_image(Image.open(img)) for img in samples] if samples else []
    console_base64 = [encode_image(Image.open(img)) for img in console] if console else []

    prompt=f'''
    you are a powerful coder. you can solve any type of coding questions. Now your role is to help your friends by solving the coding questions.
    you need to give them a very accurate code that can pass the hidden test cases also..
    you will be provided with a coding question that has to be solved, sample inputs and outputs. 
    you may also be given a function with the given parameters which is provided in the console.
    1. you have to read and analyze the coding question. 
    2. find the accurate code solution to solve the problem that can pass the given sample iputs and outputs.
    3. while generating the code please consider the below points.
        -> don't change the function names and function parameters.
        -> use the parameters that are provided in the given function parameters.
        -> don't remove any lines from the given structure of the code on the console like classes and functions.
    4. trace the code to check whether the code can be able to pass every testcase from each corner.
    5. refine the solution if needed.
    6. give the final code. don't include any introductions, explainations in the output.
    ** don't use recursion** 
    ** don't include the comments inside the function block **
    ** Ensure the time complexity should be minimum **
    '''

    input_data = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/png;base64,{que_base64}"},
                {"type": "image_url", "image_url": f"data:image/png;base64,{sample_base64}"},
                {"type": "image_url", "image_url": f"data:image/png;base64,{console_base64}"}

            ]
        }
    ]
    res=model.invoke(input_data)
    st.write(res.content)
    prompt2=f'''you are given a code.
    you need to output the explanation of the code line by line and each function used in the code but not as comments.
    The code doesn't need to be structured.
    code: {res.content}'''
    res1=model.invoke(prompt2)
    st.subheader('Explaination')
    st.write(res1.content)