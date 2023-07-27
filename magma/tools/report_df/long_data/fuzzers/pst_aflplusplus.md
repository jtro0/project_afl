---
title: pst_aflplusplus
---
{% capture template %}
<div class="section">
    <h1>pst_aflplusplus</h1>
    <p>
        This page shows the distribution of time-to-bug measurements for every bug reached and/or triggered by the
        fuzzer. The results are grouped by target to highlight any performance trends the fuzzer may have against
        specific targets.
    </p>
    <h2>libpng</h2>
        <h3>libpng_read_fuzzer</h3>
        <div class="row">
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libpng_libpng_read_fuzzer_reached.svg">
            </div>
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libpng_libpng_read_fuzzer_triggered.svg">
            </div>
        </div>
    <h2>libtiff</h2>
        <h3>tiffcp</h3>
        <div class="row">
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libtiff_tiffcp_reached.svg">
            </div>
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libtiff_tiffcp_triggered.svg">
            </div>
        </div>
    <h2>libxml2</h2>
        <h3>libxml2_xml_read_memory_fuzzer</h3>
        <div class="row">
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libxml2_libxml2_xml_read_memory_fuzzer_reached.svg">
            </div>
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libxml2_libxml2_xml_read_memory_fuzzer_triggered.svg">
            </div>
        </div>
        <h3>xmllint</h3>
        <div class="row">
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libxml2_xmllint_reached.svg">
            </div>
            <div class="col s6">
                <img class="materialboxed responsive-img" src="../plot/box_pst_aflplusplus_libxml2_xmllint_triggered.svg">
            </div>
        </div>
</div>
{% endcapture %}
{{ template | replace: '    ', ''}}
