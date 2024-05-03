import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components

def matrix_to_latex(matrix,colored_entry = None,colored_2entry = None,color="red"):
    ltx_str = "\\begin{pmatrix} \,"
    i=0
    for row in matrix:
        for col in row:
            if colored_entry == None:
                ltx_str += f" {col} \,"
            else:
                i+=1
                if i == colored_entry or i == colored_2entry:
                    ltx_str += "{\\color{"+f"{color}"+"}"+f" {col}"+ "} \,"
                else:
                    ltx_str += f" {col} \,"
        ltx_str += "\\\\"
    ltx_str += "\\end{pmatrix}"    
    return ltx_str

st.header("Corrección de errores con Hamming (4,7)")
st.write("Se considera un mensaje m, que se codifica para blindarlo contra errores.Para generar el código se multiplica el mensaje por una matriz generadora")
st.latex('''\\vec{m}G=\\vec{c}''')

st.write("Idealmente el código enviado es exactamente igual al código recibido")
st.latex('''\\vec{r}=\\vec{c}''')
st.write("Podemos verificarlo multiplicando la matriz de paridad por la respuesta que nos dará en vector síndrome z, el cuál debe valer 0")
st.latex('''\\vec{z}=H \\vec{r}^{T} = H \\vec{c}^{T} =\\vec{0}''')
st.write("Si la respuesta no es igual al código enviado, entonces")
st.latex('''\\vec{r}=\\vec{c}^{T}+\\vec{e}_{i}^{T}''')
st.write("Y al calcular el síndrome")
st.latex('''\\vec{z}=H (\\vec{c}^{T}+\\vec{e}_{i}^{T})=H \\vec{c}^{T}+ H \\vec{e}_{i}^{T}=\\vec{0}+ H \\vec{e}_{i}^{T} = H \\vec{e}_{i}^{T}''')
st.write("Donde el síndrome nos permite identificar el bit erróneo")

st.subheader("Mensaje a enviar")
st.text_input("Introduce un mensaje de 4 bits", key="message")
# You can access the value at any point with:
raw_message = st.session_state.message
list_message = [0,0,0,0]

message =  np.array([list_message]) 

if len(raw_message)==4:
    for i in range(4):
        list_message[i] = int(raw_message[i])
    message =  np.array([list_message])    
    latex_message = matrix_to_latex(message)
    st.latex("\\vec{m}="+latex_message)
    

    st.subheader("Matriz G de Hamming (4,7)")

    hamming47 = np.array([
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
        ])

    latex_hamming = matrix_to_latex(hamming47)    
    st.latex("G="+latex_hamming)

    st.subheader("Mensaje enviado")

    #Multiplicamos el mensaje por la matriz de Hamming
    message_sended = np.dot(message,hamming47)
    message_sended = message_sended%2

    latex_message_sended = matrix_to_latex(message_sended)

    st.latex("\\vec{c}="+latex_message+"\\cdot"+latex_hamming+" = " +latex_message_sended)

    st.subheader("Mensaje recibido")

    recibed_message = message_sended
    colored = None
    colored2 = None
    if st.checkbox('Intercambiar bit'):
        bit = st.slider('bit',1,7)
        recibed_message[0,bit-1]=(recibed_message[0,bit-1]+1)%2
        colored = bit

    if st.checkbox('Intercambiar otro bit'):
        bit2 = st.slider('bit 2',1,7)
        recibed_message[0,bit2-1]=(recibed_message[0,bit2-1]+1)%2
        colored2 = bit2

    latex_recibed_message = matrix_to_latex(recibed_message,colored,colored2)
    st.latex("\\vec{r}="+latex_recibed_message)

    st.subheader("Matriz de paridad H")

    hamming47_parity = np.array([
        [1, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]    
        ])

    latex_hamming47_parity = matrix_to_latex(hamming47_parity)
    st.latex("H="+latex_hamming47_parity)

    st.subheader("Revisión de paridad")
    parity_check = np.dot(hamming47_parity,recibed_message.transpose())
    parity_check = parity_check%2

    latex_recibed_message_t = matrix_to_latex(recibed_message.transpose())
    latex_parity_check = matrix_to_latex(parity_check)
    st.latex("\\vec{z}="+latex_hamming47_parity+"\\cdot"+latex_recibed_message_t+"="+latex_parity_check)


    #Evaluamos cantidad de errores
    errores = parity_check.sum() != 0
    n_bit_error = None
    


    if errores:
        col1, col2, col3, = st.columns(3)
        
        cet_latex_array=[]
        for i in range(7):
            e = [0 if b != i else 1 for b in range(7)]            
            et = np.array([e]).transpose()
            latex_et = matrix_to_latex(et)
            parity_et = np.dot(hamming47_parity,et)
            latex_parity_et = matrix_to_latex(parity_et)
            #cet_latex_array.append("H \\vec{e}_{"+str(i+1)+"}^{T}="+latex_hamming47_parity+"\\cdot"+latex_et+"="+latex_parity_et)
            cet_latex_array.append("H \\vec{e}_{"+str(i+1)+"}^{T}="+"H"+"\\cdot"+latex_et+"="+latex_parity_et)
            if np.all(parity_et==parity_check):                
                cet_latex_array[-1]="{\\color{green}"+cet_latex_array[-1]+"}"
            else:
                cet_latex_array[-1]="{\\color{orange}"+cet_latex_array[-1]+"}"
                
        with col1:
            st.latex(cet_latex_array[0])
            st.latex(cet_latex_array[3])
            st.latex(cet_latex_array[6])
            
        with col2:
            st.latex(cet_latex_array[1])
            st.latex(cet_latex_array[4])
        with col3:
            st.latex(cet_latex_array[2])
            st.latex(cet_latex_array[5])        
            
            
        for i in range(4):    
            if np.all(parity_check == hamming47[i][-3:].reshape(3,1)):
                n_bit_error = i
                st.subheader(f"Error en el bit :red[{i+1}] del mensaje")
        for i in range(3):
            if np.all(parity_check == hamming47_parity[i][-3:].reshape(3,1)):
                n_bit_error = i+4
                st.subheader(f"Error en el bit :red[{i+5}] del mensaje")
        st.write("Mensaje corregido intercambiando el bit correspondiente al vector 'e' asociado al error")
        corrected_recibed_message_t = recibed_message.transpose()
        corrected_recibed_message_t[n_bit_error]=(corrected_recibed_message_t[n_bit_error]+1)%2
        latex_corrected_recibed_message_t=matrix_to_latex(corrected_recibed_message_t.transpose(),colored,color="green")
        st.latex(latex_corrected_recibed_message_t)


    st.subheader("Mensaje final")
    mensaje_final = ""
    for i in range(4):    
        if errores:
            mensaje_final += str(corrected_recibed_message_t[i,0])
        else:    
            mensaje_final += str(recibed_message[0,i])

    st.header(mensaje_final)