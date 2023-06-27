(() => {
    "use strict";

    function t(t, e, r) {
        return e in t ? Object.defineProperty(t, e, {
            value: r,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : t[e] = r, t
    }

    function e(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var r = 0, n = new Array(e); r < e; r++) n[r] = t[r];
        return n
    }

    function r(t, r) {
        if (t) {
            if ("string" == typeof t) return e(t, r);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            return "Object" === n && t.constructor && (n = t.constructor.name), "Map" === n || "Set" === n ? Array.from(t) : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? e(t, r) : void 0
        }
    }

    function n(t) {
        return function (t) {
            if (Array.isArray(t)) return e(t)
        }(t) || function (t) {
            if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"]) return Array.from(t)
        }(t) || r(t) || function () {
            throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
        }()
    }

    var o = "".concat("https://tp.media", "/r"), u = function (t, e) {
        var r = Object.keys(e).reduce((function (t, r) {
            var n = e[r], o = t.includes("?") ? "&" : "?";
            return n ? "".concat(t).concat(o).concat(r, "=").concat(encodeURIComponent(n)) : t
        }), t);
        return r
    }, a = function (t, e) {
        var r = e.currentTarget, n = u(o, t);
        r && (r.href = n)
    };

    function c(t, e) {
        var r = Object.keys(t);
        if (Object.getOwnPropertySymbols) {
            var n = Object.getOwnPropertySymbols(t);
            e && (n = n.filter((function (e) {
                return Object.getOwnPropertyDescriptor(t, e).enumerable
            }))), r.push.apply(r, n)
        }
        return r
    }

    function i(e) {
        for (var r, n = 1; n < arguments.length; n++) r = null == arguments[n] ? {} : arguments[n], n % 2 ? c(Object(r), !0).forEach((function (n) {
            t(e, n, r[n])
        })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : c(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
        }));
        return e
    }

    var f = function (t, e) {
        return e.some((function (e) {
            return parseInt(t, 10) === parseInt(e, 10)
        }))
    };
    !function (t) {
        var e = !1;
        if ("loading" !== document.readyState) return t(), !0;
        if (window.addEventListener) return window.addEventListener("DOMContentLoaded", t, !1), !0;
        window.attachEvent("onload", (function () {
            e = !0, t()
        }));
        var r = setInterval((function () {
            return e ? (clearInterval(r), !0) : !(document && document.getElementsByTagName && document.querySelectorAll && document.body && (clearInterval(r), t(), 0))
        }), 20)
    }((function () {
        var t = function (t) {
                var e = function (t) {
                    return decodeURIComponent(t.replace(/\+/g, " "))
                }, n = {}, o = t.match(/([^?&=]+)=([^&]*)/g);
                return null == o || o.forEach((function (t) {
                    var o = function (t, e) {
                        return function (t) {
                            if (Array.isArray(t)) return t
                        }(t) || function (t, e) {
                            var r = null == t ? null : "undefined" != typeof Symbol && t[Symbol.iterator] || t["@@iterator"];
                            if (null != r) {
                                var n, o, u = [], a = !0, c = !1;
                                try {
                                    for (r = r.call(t); !(a = (n = r.next()).done) && (u.push(n.value), !e || u.length !== e); a = !0) ;
                                } catch (t) {
                                    c = !0, o = t
                                } finally {
                                    try {
                                        a || null == r.return || r.return()
                                    } finally {
                                        if (c) throw o
                                    }
                                }
                                return u
                            }
                        }(t, e) || r(t, e) || function () {
                            throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
                        }()
                    }(t.split("="), 2), u = o[0], a = o[1], c = e(u), i = e(a);
                    n[c] = i
                })), n
            }(document.querySelector('script[src*="money_script.js"]').src), e = t.marker, o = t.exclude, c = t.include,
            l = o ? o.split(",") : [], s = c ? c.split(",") : [];
        !function (t) {
            var e = t.method, r = void 0 === e ? "POST" : e, n = t.url, o = t.params, a = t.callback, c = t.body,
                i = function (t) {
                    var e = new XMLHttpRequest, f = u(n, o);
                    e.open(r, f, !0), e.send(JSON.stringify(c)), e.onreadystatechange = function () {
                        if (4 === e.readyState) {
                            if (200 === e.status) {
                                var r = JSON.parse(e.response);
                                a(r)
                            }
                            (500 === e.status || 500 < e.status) && 0 !== t && setTimeout((function () {
                                return i(t - 1)
                            }), 300)
                        }
                    }
                };
            i(3)
        }({
            method: "GET",
            url: "https://brand.travelpayouts.com/api/money_script/script_brands",
            params: {marker: e},
            callback: function (t) {
                return function (t, e) {
                    var r = e.excludes, o = e.includes, u = e.marker, c = e.timeout, l = void 0 === c ? 1e3 : c,
                        s = t.filter((function (t) {
                            return function (t, e, r) {
                                return r.length ? f(t, r) : !f(t, e)
                            }(t.campaign_id, r, o)
                        })), d = [];
                    if (s.length) {
                        var m = function () {
                            var t = function (t) {
                                var e = document.querySelectorAll("a"), r = Array.from(e).reduce((function (e, r) {
                                    var n;
                                    try {
                                        n = new URL(r.href)
                                    } catch (t) {
                                        return e
                                    }
                                    return e.push({node: r, url: n, marker: t}), e
                                }), []);
                                return r
                            }(u), e = function (t, e) {
                                return t.reduce((function (t, r) {
                                    var o = function (t, e) {
                                        return e.find((function (e) {
                                            return e.campaign_domains.some((function (e) {
                                                return -1 !== t.hostname.indexOf(e)
                                            }))
                                        }))
                                    }(r.url, e);
                                    return o ? [].concat(n(t), [i(i({}, r), o)]) : t
                                }), [])
                            }(t, s), r = function (t, e) {
                                return e.filter((function (e) {
                                    return !t.some((function (t) {
                                        return t.node === e.node
                                    }))
                                }))
                            }(d, e);
                            d = [].concat(n(d), n(r)), 0 < r.length ? (function (t) {
                                t.forEach((function (t) {
                                    var e = t.campaign_id, r = t.promo_id, n = t.node;
                                    return function (t, e, r) {
                                        var n = function (o) {
                                            r(e, o), t.removeEventListener("mousedown", n, !1), t.removeEventListener("touchstart", n, !1)
                                        };
                                        t.addEventListener("mousedown", n, !1), t.addEventListener("touchstart", n, !1)
                                    }(n, {marker: t.marker, campaign_id: e, p: r, u: n.href}, a)
                                }))
                            }(e), setTimeout(m, l)) : setTimeout(m, l)
                        };
                        m()
                    }
                }(t, {excludes: l, includes: s, marker: e, timeout: 500})
            }
        })
    }))
})();