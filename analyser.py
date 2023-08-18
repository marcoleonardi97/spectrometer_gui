import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Create the GUI
window = tk.Tk()
window.title("DIY Spectrometer")
window.resizable(0,0)  # Don't make it resizable or the grid will mess up if you move it

# These reference spectra are calculated using absorption lines and 'line_converter.py'. Could be wrong who knows
reference_spectra = {
    'Hydrogen': [0.0, 0.0, 0.0, 0.0, 0.0, 255.0, 255.0, 255.0, 0.0, 0.0, 255.0],
    'Helium': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 255.0, 255.0, 255.0],
    'Oxygen': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 255.0, 255.0, 255.0, 0.0, 255.0]}

def load_spectrum():
	"""
	Select an image file to display and analyse. The file's path is set for the match_spectrum function
	"""
	file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
	if file_path:
		path_label.configure(text=file_path)
		image = Image.open(file_path)
		#image = img.resize((800,600))
		fig, ax = plt.subplots()
		ax.imshow(image)
		ax.axis("off")
		canvas.delete("all")
		canvas2 = FigureCanvasTkAgg(fig, master=canvas)
		canvas2.draw()
		canvas2.get_tk_widget().grid(row=5,column=0, sticky="nsew")
		toolbar = NavigationToolbar2Tk(canvas2, canvas)
		toolbar.update()
		toolbar.grid(row=5,column=0, sticky="nsew")
		canvas2.get_tk_widget().grid(row=5, column=0)

def match_spec_templates():
	"""
	We can have a set of template spectra to compare the analyzed spectrum to.
	This is not really spectroscopy but it's the easiest way if we only have a few
	"""
	pass
    
def match_spectrum():
	"""
	Compares intensity distribution in two different pictures. Prob doesn't work.
	Should probably be changed to compare original ROI.
	It's way easier to have template images for the spectra, but it's less convenient
	for users - easy trick for the pp tho
	"""
    # Load and preprocess the input spectrum image
	if path_label['text'] == " " or path_label['text'] == ".png":
		result_label.configure(text="No spectrum found")
		return
	input_spectrum = path_label['text']
    # Load and preprocess the input spectrum image
	spectrum_image = cv2.imread(input_spectrum)
	spectrum_image = cv2.resize(spectrum_image, (len(reference_spectra['Hydrogen']), 1))
	_, spectrum_image = cv2.threshold(spectrum_image, 127, 255, cv2.THRESH_BINARY)

    # Calculate the sum of intensities for each column
	spectrum_values = np.sum(spectrum_image, axis=0)
	print(spectrum_values)

    # Find the best match by comparing the input spectrum with the reference spectra
	best_match = None
	best_match_diff = float('inf')
	for element, reference_spectrum in reference_spectra.items():
		adjusted_reference_spectrum = np.resize(reference_spectrum, spectrum_values.shape)
		diff = np.sum(np.abs(adjusted_reference_spectrum - spectrum_values))
		if diff < best_match_diff:
			best_match = element
			best_match_diff = diff
			"""
			This distiction can (should) be changed
			"""
			if diff > 1000:
				result = "Could not trace element from spectrum."
			elif diff > 500:
				result = f"This may be {best_match}; high uncertainty"
			else:
				result = f"This is likely {best_match}; high confidence"
			
	result_label.configure(text=result)

# Main function with video capture handling and graph plot
def main():
    cap = cv2.VideoCapture(0)
    roi_selected = False
    path_label.configure(text=f"{name_entry.get()}.png")
    
    while(True):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (800,600), interpolation=cv2.INTER_AREA)
        
        k = cv2.waitKey(1)
        
        if k & 0xFF == ord('s') and roi_selected == True:
            shape = cropped.shape
            roi_image = cropped.copy()
            roi_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB)
            roi_image = Image.fromarray(roi_image)
            roi_image = roi_image.resize((800,300),Image.ANTIALIAS)
            roi_image = ImageTk.PhotoImage(roi_image)
            roi_canvas.create_image(0,0,anchor="center", image=roi_image)
            r_dist = []
            b_dist = []
            g_dist = []
            i_dist = []
            for i in range(shape[1]):
                r_val = np.mean(cropped[:, i][:, 0])
                b_val = np.mean(cropped[:, i][:, 1])
                g_val = np.mean(cropped[:, i][:, 2])
                i_val = (r_val + b_val + g_val) / 3

                r_dist.append(r_val)
                g_dist.append(g_val)
                b_dist.append(b_val)
                i_dist.append(i_val)
            
            cv2.destroyAllWindows()
            plt.subplot(111)
            plt.imshow(frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])])
            fig = plt.figure()
            plt.subplot(111)
            plt.plot(r_dist, color='r', label='red')
            plt.plot(g_dist, color='g', label='green')
            plt.plot(b_dist, color='b', label='blue')
            plt.plot(i_dist, color='k', label='mean')
            #plt.legend(loc="upper left", framealpha=0.5)
            plt.grid(visible=True)
            plt.savefig(f"{name_entry.get()}.png", bbox_inches="tight")
            #plt.show()
            canvas.delete("all")
            canvas2 = FigureCanvasTkAgg(fig, master=canvas)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=5,column=0, sticky="nsew")
            toolbar = NavigationToolbar2Tk(canvas2, canvas)
            toolbar.update()
            toolbar.grid(row=5,column=0,sticky="nsew")
            canvas2.get_tk_widget().grid(row=5, column=0, sticky="nsew")    

        elif k & 0xFF == ord('r'):
            r = cv2.selectROI(frame)
            roi_selected = True
            
        elif k & 0xFF == ord('q'):
            break
        
        else:
            if roi_selected:
                cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                cv2.imshow('roi', cropped)
                cv2.destroyWindow('frame')
            else:
                cv2.imshow('frame', frame)
        
    cap.release()
    cv2.destroyAllWindows()


############################
# Interface Widgets Below
############################

# Path
path_label = tk.Label(window, text=" ", font=("Arial", 14))

#  Notes Box
T = tk.Text(window, height=10, width=50)
T.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
quote = """To make an analysis, here are the steps to follow:

Flash the spectrometer with a source of light
Use the R key to crop the image and press Enter.
Use the S key to get the intensity graph.
Enter a file name to save the graph as a .png
You must save the graph image to analyze it.

Attività Professionalizzante - 05/2023 - Unibo"""
T.insert(tk.END, quote)
T.config(state="disabled")

# File name for saving and retreiving path
name_label = tk.Label(window, text="Save as:")
name_label.grid(row=1, column=0)
name_entry = tk.Entry(window)
name_entry.grid(row=1, column=1)

# Start button - calls function "main"
start_button = tk.Button(window, text="Start", command=main)
start_button.grid(row=2, column=0, columnspan=2, sticky = tk.W+tk.E+tk.N)

# Load button - calls function "load_spectrum"
load_button = tk.Button(window, text="Load Spectrum", command=load_spectrum)
load_button.grid(row=3, column=0, columnspan=2, sticky = tk.NW+tk.NE, pady=10)

# Canvas to display the selected image from capture
roi_canvas = tk.Canvas(window, bd=0, highlightthickness=0, width=250, height=150)
roi_canvas.grid(row=4, column=0, columnspan=2)

# Result graph canvas
canvas = tk.Canvas(window, bd=0, highlightthickness=0, width=250, height=150)
canvas.grid(row=5, column=0, columnspan = 2, sticky="nsew")

# Find element button
an_button = tk.Button(window, text="Find Element", command=match_spectrum)
an_button.grid(row=6, column=0, columnspan=2, sticky = tk.W+tk.E)

# Display element result
result_label = tk.Label(window, text=" ", font=("Arial", 14))
result_label.grid(row=7, column=0, columnspan=2)

# Open the interface
window.mainloop()
