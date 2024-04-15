SSH Proxy Tracer
======

This tool is a proof-of-concept that BPF can be used to trace SSH proxy logs.

Imagine that you have a host that is sole role is being ssh jump host and you want to trace where exactly your users connect through it.  
With BPF it is easy you just have to trace TCP connections originating on the host.

## Building

To build a debian package you can just use provided Makefile:

```
make build_deb
```

To clean after debian package building you can use:

```
make clean_deb
```

## Acknowledges

This `C` code was derived from `tcpconnect` from [bcc](https://github.com/iovisor/bcc)!
