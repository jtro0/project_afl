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
</div>
{% endcapture %}
{{ template | replace: '    ', ''}}
