// ImageJ/Fiji HUMAN ROI collection, 100x images only. No generated grain contours.
macro "Al-GNP expert grain ROI collection 100x" {
    path = File.openDialog("Choose one original 100x BMP");
    if (path == "") exit("No BMP selected.");
    open(path);
    title = getTitle();
    // Researcher-confirmed ImageJ same-microscope ruler calibration
    run("Set Scale...", "distance=1 known=0.473 unit=um");
    run("Set Measurements...", "area perimeter shape feret's centroid display redirect=None decimal=4");
    roiManager("reset");
    waitForUser("Manual grain tracing - " + title,
      "Draw polygon/freehand boundaries only around clearly identified grains.\n" +
      "Press T to store each ROI. Do not trace ambiguous etching structures.\n" +
      "Mark unresolvable fields as such in the audit template instead.");
    n=roiManager("count");
    if(n<1)exit("No manual grain ROIs measured.");
    dir=getDirectory("Choose location for manual ROI evidence");
    if(dir=="")exit("No output path chosen.");
    roiManager("Save",dir+title+"_manual_roi.zip");
    run("Clear Results");
    roiManager("Measure");
    saveAs("Results",dir+title+"_manual_measurements.csv");
    print("Saved "+n+" HUMAN-drawn contours for "+title);
}
