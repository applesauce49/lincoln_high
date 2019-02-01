function mpmod(base, exponent, modulus) { if ((base < 1) || (exponent < 0) || (modulus < 1)) { return("invalid"); } result = 1; while (exponent > 0) { if ((exponent % 2) == 1) { result = (result \* base) % modulus; } base = (base \* base) % modulus; exponent = Math.floor(exponent / 2); } return (result); } function eulerphi(x) { result = 0; for (i = 1; i < x; i++) { if (isunit(i,x)) { result++; } } return (result); } var doccolor="ff80ff"; function shadetd(alignment) { document.write("<td bgcolor="+doccolor+" align="+alignment+">");}

![](https://www.intel.com/etc/designs/intel/clientlibs/pages/commons-page/images/intel-logo-highres.png)

> PowerMod Calculator
> -------------------
> 
> Computes (base)(exponent) mod (modulus) in log(exponent) time.
> 
> Base: 
> 
> Exponent: 
> 
> Modulus: 
> 
> _b__e_ MOD _m_ =
