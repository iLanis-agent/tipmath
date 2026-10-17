// Tip Math engine - the check, in whole cents.
// Mirrored by oracle.py; keep the op order identical.

function _cents(x) {
  return Math.floor(x * 100 + 0.5);
}

function _usd(c) {
  var d = Math.floor(c / 100), r = c % 100;
  var s = String(d), out = "";
  while (s.length > 3) { out = "," + s.slice(-3) + out; s = s.slice(0, -3); }
  return "$" + s + out + "." + (r < 10 ? "0" : "") + r;
}

function _money(x, msg) {
  if (!isFinite(x) || x <= 0) throw new Error(msg);
  return _cents(x);
}

function _pct(x, msg) {
  if (!isFinite(x) || x < 0 || x > 100) throw new Error(msg);
  return x;
}

// The tip truth: your percent, on the amount you chose, in cents.
function tipTruth(subtotal, tipPct) {
  var sc = _money(subtotal, "enter a bill over $0");
  _pct(tipPct, "tip percent must be 0 to 100");
  var tc = Math.floor(sc * tipPct / 100 + 0.5);
  return tipPct + "% of " + _usd(sc) + " is " + _usd(tc) + " - the check comes to " + _usd(sc + tc) + ".";
}

// The tax truth: tipping on the pre-tax or the post-tax number.
function taxTruth(subtotal, taxPct, tipPct) {
  var sc = _money(subtotal, "enter a bill over $0");
  _pct(taxPct, "tax percent must be 0 to 100");
  _pct(tipPct, "tip percent must be 0 to 100");
  var taxC = Math.floor(sc * taxPct / 100 + 0.5);
  var pre = Math.floor(sc * tipPct / 100 + 0.5);
  var post = Math.floor((sc + taxC) * tipPct / 100 + 0.5);
  var diff = post - pre;
  var head = "Tip on " + _usd(sc) + " is " + _usd(pre) + "; on " + _usd(sc + taxC) + " with tax it is " + _usd(post);
  if (diff === 0) return head + " - no difference.";
  return head + " - tipping on the tax costs " + _usd(diff) + " more.";
}

// The split truth: whole cents, nobody shorted.
function splitTruth(total, people) {
  var tc = _money(total, "enter a total over $0");
  if (!isFinite(people) || people < 1 || people !== Math.floor(people)) {
    throw new Error("people must be a whole number, at least 1");
  }
  var base = Math.floor(tc / people), extra = tc % people;
  if (people === 1) return _usd(tc) + " for one person is " + _usd(tc) + ".";
  if (extra === 0) return _usd(tc) + " across " + people + " is " + _usd(base) + " each, exactly.";
  var lo = people - extra;
  return _usd(tc) + " across " + people + " is " + _usd(base) + " each with " + extra +
    " cent" + (extra === 1 ? "" : "s") + " left over - " + extra + " " + (extra === 1 ? "person pays " : "people pay ") +
    _usd(base + 1) + " and " + lo + " " + (lo === 1 ? "pays " : "pay ") + _usd(base) + ".";
}
