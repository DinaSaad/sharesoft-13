/*!
 * Pusher JavaScript Library v1.9.6
 * http://pusherapp.com/
 *
 * Copyright 2011, Pusher
 * Released under the MIT licence.
 */

if (typeof Function.prototype.scopedTo === "undefined") Function.prototype.scopedTo = function (a, c) {
        var b = this;
        return function () {
            return b.apply(a, Array.prototype.slice.call(c || []).concat(Array.prototype.slice.call(arguments)))
        }
};
var Pusher = function (a, c) {
    this.options = c || {};
    this.path = "/app/" + a + "?client=js&version=" + Pusher.VERSION;
    this.key = a;
    this.channels = new Pusher.Channels;
    this.global_channel = new Pusher.Channel("pusher_global_channel");
    this.global_channel.global = !0;
    var b = this;
    this.connection = new Pusher.Connection(this.key, this.options);
    this.connection.bind("connected", function () {
        b.subscribeAll()
    }).bind("message", function (a) {
        b.send_local_event(a.event, a.data, a.channel)
    }).bind("disconnected", function () {
        b.channels.disconnect()
    }).bind("error", function (a) {
        Pusher.debug("Error", a)
    });
    Pusher.instances.push(this);
    Pusher.isReady && b.connect()
};
Pusher.instances = [];
Pusher.prototype = {
    channel: function (a) {
        return this.channels.find(a)
    },
    connect: function () {
        this.connection.connect()
    },
    disconnect: function () {
        this.connection.disconnect()
    },
    bind: function (a, c) {
        this.global_channel.bind(a, c);
        return this
    },
    bind_all: function (a) {
        this.global_channel.bind_all(a);
        return this
    },
    subscribeAll: function () {
        for (var a in this.channels.channels) this.channels.channels.hasOwnProperty(a) && this.subscribe(a)
    },
    subscribe: function (a) {
        var c = this,
            b = this.channels.add(a, this);
        this.connection.state === "connected" &&
            b.authorize(this, function (e, f) {
            e ? b.emit("subscription_error", f) : c.send_event("pusher:subscribe", {
                channel: a,
                auth: f.auth,
                channel_data: f.channel_data
            })
        });
        return b
    },
    unsubscribe: function (a) {
        this.channels.remove(a);
        this.connection.state === "connected" && this.send_event("pusher:unsubscribe", {
            channel: a
        })
    },
    send_event: function (a, c, b) {
        Pusher.debug("Event sent (channel,event,data)", b, a, c);
        a = {
            event: a,
            data: c
        };
        b && (a.channel = b);
        this.connection.send(JSON.stringify(a));
        return this
    },
    send_local_event: function (a, c, b) {
        c =
            Pusher.data_decorator(a, c);
        b ? (b = this.channel(b)) && b.dispatch_with_all(a, c) : Pusher.debug("Event recd (event,data)", a, c);
        this.global_channel.dispatch_with_all(a, c)
    }
};
Pusher.Util = {
    extend: function extend(c, b) {
        for (var e in b) c[e] = b[e] && b[e].constructor && b[e].constructor === Object ? extend(c[e] || {}, b[e]) : b[e];
        return c
    }
};
Pusher.debug = function () {
    if (Pusher.log) {
        for (var a = ["Pusher"], c = 0; c < arguments.length; c++) typeof arguments[c] === "string" ? a.push(arguments[c]) : window.JSON == void 0 ? a.push(arguments[c].toString()) : a.push(JSON.stringify(arguments[c]));
        Pusher.log(a.join(" : "))
    }
};
Pusher.VERSION = "1.9.6";
Pusher.host = "ws.pusherapp.com";
Pusher.ws_port = 80;
Pusher.wss_port = 443;
Pusher.channel_auth_endpoint = "/pusher/auth";
Pusher.connection_timeout = 5E3;
Pusher.cdn_http = "http://js.pusherapp.com/";
Pusher.cdn_https = "https://d3ds63zw57jt09.cloudfront.net/";
Pusher.dependency_suffix = ".min";
Pusher.data_decorator = function (a, c) {
    return c
};
Pusher.allow_reconnect = !0;
Pusher.channel_auth_transport = "ajax";
Pusher.isReady = !1;
Pusher.ready = function () {
    Pusher.isReady = !0;
    for (var a = 0, c = Pusher.instances.length; a < c; a++) Pusher.instances[a].connect()
};
(function () {
    function a() {
        this.callbacks = {};
        this.global_callbacks = []
    }
    a.prototype.bind = function (a, b) {
        this.callbacks[a] = this.callbacks[a] || [];
        this.callbacks[a].push(b);
        return this
    };
    a.prototype.emit = function (a, b) {
        this.dispatch_global_callbacks(a, b);
        this.dispatch(a, b);
        return this
    };
    a.prototype.bind_all = function (a) {
        this.global_callbacks.push(a);
        return this
    };
    a.prototype.dispatch = function (a, b) {
        var e = this.callbacks[a];
        if (e) for (var f = 0; f < e.length; f++) e[f](b);
        else !this.global && !(this instanceof Pusher.Connection ||
            this instanceof Pusher.Machine) && Pusher.debug("No callbacks for " + a, b)
    };
    a.prototype.dispatch_global_callbacks = function (a, b) {
        for (var e = 0; e < this.global_callbacks.length; e++) this.global_callbacks[e](a, b)
    };
    a.prototype.dispatch_with_all = function (a, b) {
        this.dispatch(a, b);
        this.dispatch_global_callbacks(a, b)
    };
    this.Pusher.EventsDispatcher = a
}).call(this);
(function () {
    function a(a, b) {
        if (a == null) return -1;
        if (f && a.indexOf === f) return a.indexOf(b);
        for (i = 0, l = a.length; i < l; i++) if (a[i] === b) return i;
        return -1
    }
    function c(a, b, c) {
        if (b[a] !== void 0) b[a](c)
    }
    function b(a, b, c, f) {
        e.EventsDispatcher.call(this);
        this.actor = a;
        this.state = void 0;
        this.errors = [];
        this.stateActions = f;
        this.transitions = c;
        this.transition(b)
    }
    var e = this.Pusher,
        f = Array.prototype.indexOf;
    b.prototype.transition = function (b, e) {
        var f = this.state,
            h = this.stateActions;
        if (f && a(this.transitions[f], b) == -1) throw Error(this.actor.key +
                ": Invalid transition [" + f + " to " + b + "]");
        c(f + "Exit", h, e);
        c(f + "To" + (b.substr(0, 1).toUpperCase() + b.substr(1)), h, e);
        c(b + "Pre", h, e);
        this.state = b;
        this.emit("state_change", {
            oldState: f,
            newState: b
        });
        c(b + "Post", h, e)
    };
    b.prototype.is = function (a) {
        return this.state === a
    };
    b.prototype.isNot = function (a) {
        return this.state !== a
    };
    e.Util.extend(b.prototype, e.EventsDispatcher.prototype);
    this.Pusher.Machine = b
}).call(this);
(function () {
    function a(a) {
        a.connectionWait = 0;
        a.openTimeout = b.TransportType === "flash" ? 5E3 : 2E3;
        a.connectedTimeout = 2E3;
        a.connectionSecure = a.compulsorySecure;
        a.connectionAttempts = 0
    }
    function c(c, e) {
        function m() {
            d.connectionWait < h && (d.connectionWait += k);
            d.openTimeout < s && (d.openTimeout += g);
            d.connectedTimeout < t && (d.connectedTimeout += p);
            if (d.compulsorySecure !== !0) d.connectionSecure = !d.connectionSecure;
            d.connectionAttempts++
        }
        function q() {
            d._machine.transition("impermanentlyClosing")
        }
        function u() {
            d._machine.transition("open")
        }

        function r(a) {
            var c;
            a: {
                try {
                    var e = JSON.parse(a.data);
                    if (typeof e.data === "string") try {
                            e.data = JSON.parse(e.data)
                    } catch (f) {
                        if (!(f instanceof SyntaxError)) throw f;
                    }
                    c = e;
                    break a
                } catch (h) {
                    d.emit("error", {
                        type: "MessageParseError",
                        error: h,
                        data: a.data
                    })
                }
                c = void 0
            }
            if (typeof c !== "undefined") if (b.debug("Event recd (event,data)", c.event, c.data), c.event === "pusher:connection_established") d._machine.transition("connected", c.data.socket_id);
                else if (c.event === "pusher:error") {
                if (d.emit("error", {
                    type: "PusherError",
                    data: c.data
                }),
                    c.data.code === 4001 && d._machine.transition("permanentlyClosing"), c.data.code === 4E3) b.debug(c.data.message), d.compulsorySecure = !0, d.connectionSecure = !0, d.options.encrypted = !0
            } else c.event !== "pusher:heartbeat" && d._machine.is("connected") && d.emit("message", c)
        }
        function n() {
            d._machine.transition("waiting")
        }
        function o() {
            d.emit("error", {
                type: "WebSocketError"
            });
            d.socket.close();
            d._machine.transition("impermanentlyClosing")
        }
        function j(a, c) {
            if (d.state !== a) {
                var e = d.state;
                d.state = a;
                b.debug("State changed", e + " -> " +
                    a);
                d.emit("state_change", {
                    previous: e,
                    current: a
                });
                d.emit(a, c)
            }
        }
        var d = this;
        b.EventsDispatcher.call(this);
        this.options = b.Util.extend({
            encrypted: !1
        }, e || {});
        this.netInfo = new b.NetInfo;
        this.netInfo.bind("online", function () {
            d._machine.is("waiting") && (d._machine.transition("connecting"), j("connecting"))
        });
        this.netInfo.bind("offline", function () {
            if (d._machine.is("connected")) d.socket.onclose = void 0, d.socket.onmessage = void 0, d.socket.onerror = void 0, d.socket.onopen = void 0, d.socket.close(), d.socket = void 0, d._machine.transition("waiting")
        });
        this._machine = new b.Machine(d, "initialized", f, {
            initializedPre: function () {
                d.compulsorySecure = d.options.encrypted;
                d.key = c;
                d.socket = null;
                d.socket_id = null;
                d.state = "initialized"
            },
            waitingPre: function () {
                d.connectionWait > 0 && d.emit("connecting_in", d.connectionWait);
                d.netInfo.isOnLine() === !1 || d.connectionAttempts > 4 ? j("unavailable") : j("connecting");
                if (d.netInfo.isOnLine() === !0) d._waitingTimer = setTimeout(function () {
                        d._machine.transition("connecting")
                    }, d.connectionWait)
            },
            waitingExit: function () {
                clearTimeout(d._waitingTimer)
            },
            connectingPre: function () {
                if (d.netInfo.isOnLine() === !1) d._machine.transition("waiting"), j("unavailable");
                else {
                    var a;
                    a = b.ws_port;
                    var c = "ws://";
                    if (d.connectionSecure || document.location.protocol === "https:") a = b.wss_port, c = "wss://";
                    a = c + b.host + ":" + a + "/app/" + d.key + "?client=js&version=" + b.VERSION;
                    b.debug("Connecting", a);
                    d.socket = new b.Transport(a);
                    d.socket.onopen = u;
                    d.socket.onclose = n;
                    d.socket.onerror = o;
                    d._connectingTimer = setTimeout(q, d.openTimeout)
                }
            },
            connectingExit: function () {
                clearTimeout(d._connectingTimer)
            },
            connectingToWaiting: function () {
                m()
            },
            connectingToImpermanentlyClosing: function () {
                m()
            },
            openPre: function () {
                d.socket.onmessage = r;
                d.socket.onerror = o;
                d.socket.onclose = n;
                d._openTimer = setTimeout(q, d.connectedTimeout)
            },
            openExit: function () {
                clearTimeout(d._openTimer)
            },
            openToWaiting: function () {
                m()
            },
            openToImpermanentlyClosing: function () {
                m()
            },
            connectedPre: function (b) {
                d.socket_id = b;
                d.socket.onmessage = r;
                d.socket.onerror = o;
                d.socket.onclose = n;
                a(d)
            },
            connectedPost: function () {
                j("connected")
            },
            connectedExit: function () {
                j("disconnected")
            },
            impermanentlyClosingPost: function () {
                if (d.socket) d.socket.onclose = n, d.socket.close()
            },
            permanentlyClosingPost: function () {
                d.socket ? (d.socket.onclose = function () {
                    a(d);
                    d._machine.transition("permanentlyClosed")
                }, d.socket.close()) : (a(d), d._machine.transition("permanentlyClosed"))
            },
            failedPre: function () {
                j("failed");
                b.debug("WebSockets are not available in this browser.")
            }
        })
    }
    var b = this.Pusher,
        e = function () {
            var a = this;
            b.EventsDispatcher.call(this);
            window.addEventListener !== void 0 && (window.addEventListener("online", function () {
                a.emit("online", null)
            }, !1), window.addEventListener("offline", function () {
                a.emit("offline", null)
            }, !1))
        };
    e.prototype.isOnLine = function () {
        return window.navigator.onLine === void 0 ? !0 : window.navigator.onLine
    };
    b.Util.extend(e.prototype, b.EventsDispatcher.prototype);
    this.Pusher.NetInfo = b.NetInfo = e;
    var f = {
        initialized: ["waiting", "failed"],
        waiting: ["connecting", "permanentlyClosed"],
        connecting: ["open", "permanentlyClosing", "impermanentlyClosing", "waiting"],
        open: ["connected", "permanentlyClosing", "impermanentlyClosing",
                "waiting"
        ],
        connected: ["permanentlyClosing", "impermanentlyClosing", "waiting"],
        impermanentlyClosing: ["waiting", "permanentlyClosing"],
        permanentlyClosing: ["permanentlyClosed"],
        permanentlyClosed: ["waiting"],
        failed: ["permanentlyClosing"]
    }, k = 2E3,
        g = 2E3,
        p = 2E3,
        h = 5 * k,
        s = 5 * g,
        t = 5 * p;
    c.prototype.connect = function () {
        b.Transport === null || typeof b.Transport === "undefined" ? this._machine.transition("failed") : this._machine.is("initialized") ? (a(this), this._machine.transition("waiting")) : this._machine.is("waiting") && this.netInfo.isOnLine() === !0 ? this._machine.transition("connecting") : this._machine.is("permanentlyClosed") && this._machine.transition("waiting")
    };
    c.prototype.send = function (a) {
        return this._machine.is("connected") ? (this.socket.send(a), !0) : !1
    };
    c.prototype.disconnect = function () {
        this._machine.is("permanentlyClosed") || (b.debug("Disconnecting"), this._machine.is("waiting") ? this._machine.transition("permanentlyClosed") : this._machine.transition("permanentlyClosing"))
    };
    b.Util.extend(c.prototype, b.EventsDispatcher.prototype);
    this.Pusher.Connection =
        c
}).call(this);
Pusher.Channels = function () {
    this.channels = {}
};
Pusher.Channels.prototype = {
    add: function (a, c) {
        var b = this.find(a);
        b || (b = Pusher.Channel.factory(a, c), this.channels[a] = b);
        return b
    },
    find: function (a) {
        return this.channels[a]
    },
    remove: function (a) {
        delete this.channels[a]
    },
    disconnect: function () {
        for (var a in this.channels) this.channels[a].disconnect()
    }
};
Pusher.Channel = function (a, c) {
    Pusher.EventsDispatcher.call(this);
    this.pusher = c;
    this.name = a;
    this.subscribed = !1
};
Pusher.Channel.prototype = {
    init: function () {},
    disconnect: function () {},
    acknowledge_subscription: function () {
        this.subscribed = !0
    },
    is_private: function () {
        return !1
    },
    is_presence: function () {
        return !1
    },
    authorize: function (a, c) {
        c(!1, {})
    },
    trigger: function (a, c) {
        this.pusher.send_event(a, c, this.name);
        return this
    }
};
Pusher.Util.extend(Pusher.Channel.prototype, Pusher.EventsDispatcher.prototype);
Pusher.auth_callbacks = {};
Pusher.authorizers = {
    ajax: function (a, c) {
        var b;
        b = Pusher.XHR ? new Pusher.XHR : window.XMLHttpRequest ? new window.XMLHttpRequest : new ActiveXObject("Microsoft.XMLHTTP");
        b.open("POST", Pusher.channel_auth_endpoint, !0);
        b.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        b.onreadystatechange = function () {
            if (b.readyState == 4) if (b.status == 200) {
                    var a, f = !1;
                    try {
                        a = JSON.parse(b.responseText), f = !0
                    } catch (k) {
                        c(!0, "JSON returned from webapp was invalid, yet status code was 200. Data was: " + b.responseText)
                    }
                    f &&
                        c(!1, a)
                } else Pusher.debug("Couldn't get auth info from your webapp", status), c(!0, b.status)
        };
        b.send("socket_id=" + encodeURIComponent(a.connection.socket_id) + "&channel_name=" + encodeURIComponent(this.name))
    },
    jsonp: function (a, c) {
        var b = "socket_id=" + encodeURIComponent(a.connection.socket_id) + "&channel_name=" + encodeURIComponent(this.name),
            e = document.createElement("script");
        Pusher.auth_callbacks[this.name] = function (a) {
            c(!1, a)
        };
        e.src = Pusher.channel_auth_endpoint + "?callback=" + encodeURIComponent("Pusher.auth_callbacks['" +
            this.name + "']") + "&" + b;
        b = document.getElementsByTagName("head")[0] || document.documentElement;
        b.insertBefore(e, b.firstChild)
    }
};
Pusher.Channel.PrivateChannel = {
    is_private: function () {
        return !0
    },
    authorize: function (a, c) {
        Pusher.authorizers[Pusher.channel_auth_transport].scopedTo(this)(a, c)
    }
};
Pusher.Channel.PresenceChannel = {
    init: function () {
        this.bind("pusher_internal:subscription_succeeded", function (a) {
            this.acknowledge_subscription(a);
            this.dispatch_with_all("pusher:subscription_succeeded", this.members)
        }.scopedTo(this));
        this.bind("pusher_internal:member_added", function (a) {
            this.dispatch_with_all("pusher:member_added", this.members.add(a.user_id, a.user_info))
        }.scopedTo(this));
        this.bind("pusher_internal:member_removed", function (a) {
            (a = this.members.remove(a.user_id)) && this.dispatch_with_all("pusher:member_removed",
                a)
        }.scopedTo(this))
    },
    disconnect: function () {
        this.members.clear()
    },
    acknowledge_subscription: function (a) {
        this.members._members_map = a.presence.hash;
        this.members.count = a.presence.count;
        this.subscribed = !0
    },
    is_presence: function () {
        return !0
    },
    members: {
        _members_map: {},
        count: 0,
        each: function (a) {
            for (var c in this._members_map) a({
                    id: c,
                    info: this._members_map[c]
                })
        },
        add: function (a, c) {
            this._members_map[a] = c;
            this.count++;
            return this.get(a)
        },
        remove: function (a) {
            var c = this.get(a);
            c && (delete this._members_map[a], this.count--);
            return c
        },
        get: function (a) {
            return this._members_map.hasOwnProperty(a) ? {
                id: a,
                info: this._members_map[a]
            } : null
        },
        clear: function () {
            this._members_map = {};
            this.count = 0
        }
    }
};
Pusher.Channel.factory = function (a, c) {
    var b = new Pusher.Channel(a, c);
    a.indexOf(Pusher.Channel.private_prefix) === 0 ? Pusher.Util.extend(b, Pusher.Channel.PrivateChannel) : a.indexOf(Pusher.Channel.presence_prefix) === 0 && (Pusher.Util.extend(b, Pusher.Channel.PrivateChannel), Pusher.Util.extend(b, Pusher.Channel.PresenceChannel));
    b.init();
    return b
};
Pusher.Channel.private_prefix = "private-";
Pusher.Channel.presence_prefix = "presence-";
var _require = function () {
    var a;
    a = document.addEventListener ? function (a, b) {
        a.addEventListener("load", b, !1)
    } : function (a, b) {
        a.attachEvent("onreadystatechange", function () {
            (a.readyState == "loaded" || a.readyState == "complete") && b()
        })
    };
    return function (c, b) {
        function e(b, c) {
            var c = c || function () {}, e = document.getElementsByTagName("head")[0],
                g = document.createElement("script");
            g.setAttribute("src", b);
            g.setAttribute("type", "text/javascript");
            g.setAttribute("async", !0);
            a(g, function () {
                var a = c;
                f++;
                k == f && setTimeout(a, 0)
            });
            e.appendChild(g)
        }
        for (var f = 0, k = c.length, g = 0; g < k; g++) e(c[g], b)
    }
}();
(function () {
    var a = (document.location.protocol == "http:" ? Pusher.cdn_http : Pusher.cdn_https) + Pusher.VERSION,
        c = [];
    typeof window.JSON === "undefined" && c.push(a + "/json2" + Pusher.dependency_suffix + ".js");
    if (typeof window.WebSocket === "undefined" && typeof window.MozWebSocket === "undefined") window.WEB_SOCKET_DISABLE_AUTO_INITIALIZATION = !0, c.push(a + "/flashfallback" + Pusher.dependency_suffix + ".js");
    var b = function () {
        return typeof window.WebSocket === "undefined" && typeof window.MozWebSocket === "undefined" ? function () {
            typeof window.WebSocket !==
                "undefined" && typeof window.MozWebSocket === "undefined" ? (Pusher.Transport = window.WebSocket, Pusher.TransportType = "flash", window.WEB_SOCKET_SWF_LOCATION = a + "/WebSocketMain.swf", WebSocket.__addTask(function () {
                Pusher.ready()
            }), WebSocket.__initialize()) : (Pusher.Transport = null, Pusher.TransportType = "none", Pusher.ready())
        } : function () {
            Pusher.Transport = typeof window.MozWebSocket !== "undefined" ? window.MozWebSocket : window.WebSocket;
            Pusher.TransportType = "native";
            Pusher.ready()
        }
    }(),
        e = function (a) {
            var b = function () {
                document.body ?
                    a() : setTimeout(b, 0)
            };
            b()
        }, f = function () {
            e(b)
        };
    c.length > 0 ? _require(c, f) : f()
})();