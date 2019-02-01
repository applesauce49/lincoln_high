
<!--function mpmod(base, exponent, modulus) { if ((base < 1) || (exponent < 0) || (modulus < 1)) { return("invalid"); } result = 1; while (exponent > 0) { if ((exponent % 2) == 1) { result = (result \* base) % modulus; } base = (base \* base) % modulus; exponent = Math.floor(exponent / 2); } return (result); } function eulerphi(x) { result = 0; for (i = 1; i < x; i++) { if (isunit(i,x)) { result++; } } return (result); } var doccolor="ff80ff"; function shadetd(alignment) { document.write("<td bgcolor="+doccolor+" align="+alignment+">");} -->

<h2>PowerMod Calculator</h2>
Computes (base)<sup>(exponent)</sup> mod (modulus)
in log(exponent) time.
<p>

<form name=powermod>
<table border=1>
<tr>
<td>Base: 
<input type=text value="" name=pmbase
onChange="pmout.value='';"></td>
<td>Exponent:
<input type=text value="" name=pmexp
onChange="pmout.value='';"></td>
<td>Modulus:
<input type=text value="" name=pmmod
onChange="pmout.value='';"></td>
</tr>
<tr>
<td>
<input type=button value="Compute"
onClick="pmout.value=mpmod(pmbase.value, pmexp.value, pmmod.value);">
</td>
<td align=right>
<i>b</i><sup><i>e</i></sup> <font size=-1>MOD</font> <i>m</i> =
</td>
<td bgcolor=bbbbbb><input type=text value="" name=pmout
onChange="pmout.value='';">
</td>
</tr>
</table>
</form>
<p>
