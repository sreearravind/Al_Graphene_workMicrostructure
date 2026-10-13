// Phase 1 / Task 4: HUMAN expert ImageJ polygon/freehand ROI archiving.
// 100x original BMP only. This macro cannot create artificial/manual labels.
// Source: Optical miscrostructure_Figures_BMP file / correct condition folder.

macro "Al-GNP trace real 100x grain ROIs (working specimen label)" {
    sampleCodes = split("S01|S02|S03|S04|S05|S06|S07|S08|S09|S10|S11|S12","|");
    sourceDirs = split("0-500 - Copy|0-550 - Copy|0-600 - Copy|2-500 - Copy|2-550 - Copy|2-600 - Copy|3.500 - Copy|3-550 - Copy|3-600 - Copy|4-500 - Copy|4-550 - Copy|4.600 - Copy","|");
    path = File.openDialog("Choose an ORIGINAL 100x BMP image");
    if(path=="") exit("No source BMP selected.");
    code = getString("Enter working sample ID and field (e.g., S02_F1)", "S02_F1");
    splitIndex = indexOf(code,"_F");
    if(splitIndex < 0) exit("Field code must be S02_F1 style.");
    sample = substring(code,0,splitIndex);
    field = substring(code,splitIndex+2);
    idx = -1;
    for(i=0;i<lengthOf(sampleCodes);i++)
        if(sample==sampleCodes[i]) idx=i;
    if(idx < 0) exit("Unknown sample code.");
    if(indexOf(path,sourceDirs[idx]) < 0) exit("Source folder does NOT match the entered specimen ID.");
    expected = "100x"+field+".bmp";
    if(!endsWith(path,expected)) exit("Source filename does NOT match entered field number.");
    open(path);
    // ImageJ ruler reference from the SAME microscope, as researcher confirmed.
    // Use this only if camera, zoom, cropping and optical 100x acquisition are comparable.
    run("Set Scale...", "distance=1 known=0.473 unit=um");
    run("Set Measurements...", "area perimeter shape feret's centroid display redirect=None decimal=4");
    roiManager("reset");
    waitForUser("Trace actual grains: "+code,
      "Draw only clear, closed physical grain boundaries with polygon or freehand selection.\n"+
      "Press T to store EACH grain in ROI Manager.\n"+
      "Sample across the image (4 columns x 3 rows); aim for 2 clear grains per sector.\n"+
      "DO NOT trace pores, scratches, dark clusters or uncertain etch patterns as grains.\n"+
      "If field boundaries are unresolved, cancel and mark UNRESOLVABLE in the review log.");
    n=roiManager("count");
    if(n<2) exit("At least two real polygons are needed for a ZIP archive; log unresolved/insufficient field separately.");
    dir=getDirectory("Choose destination to save ImageJ manual ROIs");
    if(dir=="") exit("No output folder selected.");
    target=dir+code+".zip";
    if(File.exists(target)) exit("Target exists: do not overwrite existing ROI evidence.");
    roiManager("Save",target);
    run("Clear Results");
    roiManager("Measure");
    saveAs("Results",dir+code+"_manual_measurements.csv");
    print("Saved "+n+" manually traced ROIs for "+code+" and matching ImageJ measurements.");
    print("Record expert initials, review date, boundary confidence and exclusion notes.");
}
