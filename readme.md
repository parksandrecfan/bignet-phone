<!DOCTYPE html>
<html>
<head>
</head>
<body>

<h1>BIGNet - Phone</h1>
<h4><a href="https://drive.google.com/file/d/1qFROn8uz7wG6HjcUkMC8Rdc0atgCuA22/view?usp=share_link">[Paper]</a></h4>

<p>This page is the implementation of BIGNet in the phone case study. Car case study implementation can be found <a href="https://github.com/parksandrecfan/bignet-car"><b>here</b>.</p>
<h2>Project summary</h2>
<p>Identifying and codifying brand-related aesthetic features for produc redesign is essential yet challenging, even for humans. This project demonstrates a deep learning, data-driven way to automatically learn brand-related features through SVG-based supervised learning, using brand identification graph neural network (<b>BIGNet</b>), a hierarichal graph neural network.</p>

<p>Our approach conducting the phone study can be summarized in this flow chart:</p>
<img src="data/flowchart.png" width="1000">

<h2>System requirements</h2>
<p>The hardware information can be found in <b>Hardware Overview.txt</b>.</p>
<p>The required (Python) packages can be found in <b>requirements.txt</b>.</p>
<p>In addition, <a href="https://potrace.sourceforge.net/"><b>potrace</b></a></b> has to be downloaded to create dataset (step 1).</p>

<h2>Instruction</h2>
<p>An easy-to-follow process is to <b>run the jupyter notebooks in order from 0~7</b>. However, we did provide all the staged results to save implementers time. Downloading the GNN-dataset can skip step 1, and downloading the trained model can skip step 2, and they can both be time-consuming to run. More details are described below.</p>
<h3>Code structure</h3>
<p>All utility functions are in the <b>util directory folder</b>. The individual notebooks call from the utility folders' functions and demonstrate each step in sections.</p>
<h3>Dataset</h3>
<img src="data/dataset.png" width="1000">
<p>The synthetic SVG dataset is generated by parameter interpolation. The parameters are measured manually in dim.xlsx.</p>
<p>Running 0.phone parameters.ipynb will then initialize the measured parameters from dim.xlsx. You may also download </p>
<p>Next, the synthesis code is in 1.create_dataset.ipynb. The results generated will locate at pkl directory. The relationship of parameter names and phone features are shown in the following figure:</p>
<h3>iPhone:</h3>
<img src="data/iphone1.png" width="400">
<img src="data/iphone2.png" width="700">
<img src="data/iphone3.png" width="620">
<h3>Samsung:</h3>
<img src="data/samsung1.png" width="1000">
<img src="data/samsung2.png" width="1000">
<p>Instead of generating synthetic data from scratch, one can also directly download the SVG dataset from <a href=https://drive.google.com/file/d/1EHMhK5YhudFL1mEfMslS2hXQ92VLCOcK/view?usp=sharing><b>here</b></a>.</p>
<p>The SVG data are reprocessed to a BIGNet-friendly format. One can use this function in util to process from SVG data. One can also directly download the pickle format <a href=https://drive.google.com/file/d/1FgSsBIPzOgKaXGAYXavOU56oW8111gu4/view?usp=sharing><b>here</b></a>. Do note that to continue down the pipeline, put the decompressed data in a "pkl" directory.</p>
<h3>Training</h3>
<p>Training takes 8 formatted pickle files (train/test data/curve label/brand label/distance matrix). Train/test accuracy/loss curves are saved as well. The trained model can be downloaded here.</p>

<h3>Evaluation</h3>
<p>Dimension reduction of 2D/3D PCA/tSNE is done in 3.dimension reduction.ipynb.</p>
<img src="data/fig5.png" width="1000">
<p>Leave-one-feature-out is implemented in ablation study.ipynb. You can find the brand-relevant and irrelevant features in the ablation folder. Here are some examples. The partial (1000 samples) set of visualization results can be downloaded <a href="https://drive.google.com/file/d/1PwrxeLgwya7I41y2onD2hgMjsjUyvFD0/view?usp=share_link">here</a>.</p>
<img src="data/fig6.png" width="1000">
<p>From the LOFO result we can summarize the following brand-relevant features.</p>
<img src="data/lofo summary.png" width="800">
<p><b>Parameter exrapolation study</b></p>
<p>We performed extrapolation 3 following experiments:</p>
<p>* Apple's lens horizontal location -> extrapolation iphone width.ipynb</p>
<img src="data/Apple Phone Confidence vs Width.jpg" width="1000">
<p>* Apple's width and fillet radius -> extrapolation lens1p.ipynb</p>
<img src="data/Apple Confidence vs lens location.jpg" width="1000">
<p>* Samsung's gap from screen-frame -> extrapolation samsung scr2pl2edge.ipynb</p>
<img src="data/Samsung Screen-plane-edge Gap Heatmap.jpg" width="500">


<p>For any questions implementing, feel free to email Sean Chen as yuhsuan2@andrew.cmu.edu</p>

</body>
</html>
