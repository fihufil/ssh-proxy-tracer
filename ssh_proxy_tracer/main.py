#!/usr/bin/env python3
import pwd
from socket import AF_INET, AF_INET6, inet_ntop
from struct import pack

from bcc import BPF

VERSION = 1.0


def read_bpf_prog(prog_name):
    with open(prog_name) as prog_c:
        return prog_c.read()


class ConnTracer:
    def __init__(self):
        self.b = BPF(text=read_bpf_prog('bpf_tcp_connect.c'))
        self.b.attach_kprobe(event="tcp_v4_connect", fn_name="trace_connect_entry")
        self.b.attach_kprobe(event="tcp_v6_connect", fn_name="trace_connect_entry")
        self.b.attach_kretprobe(event="tcp_v4_connect", fn_name="trace_connect_v4_return")
        self.b.attach_kretprobe(event="tcp_v6_connect", fn_name="trace_connect_v6_return")
        # read events
        self.b["ipv4_events"].open_perf_buffer(self.print_ipv4_event)
        self.b["ipv6_events"].open_perf_buffer(self.print_ipv6_event)

    @staticmethod
    def decode_ipaddr(ipver, ipaddr):
        if ipver == 4:
            return inet_ntop(AF_INET, pack("I", ipaddr))
        else:
            return inet_ntop(AF_INET6, ipaddr)

    @staticmethod
    def get_user_name(uid):
        return pwd.getpwuid(uid).pw_name

    def print_ip_event(self, event):
        return (
            f"User {self.get_user_name(event.uid)} process {event.task.decode()}[{event.pid}] connection from "
            f"{self.decode_ipaddr(event.ip, event.saddr)}:{event.sport} to "
            f"{self.decode_ipaddr(event.ip, event.daddr)}:{event.dport}"
        )

    def print_ipv4_event(self, cpu, data, size):
        event = self.b["ipv4_events"].event(data)
        print(self.print_ip_event(event))

    def print_ipv6_event(self, cpu, data, size):
        event = self.b["ipv6_events"].event(data)
        print(self.print_ip_event(event))

    def run(self):
        print("Tracer started")
        while True:
            try:
                self.b.perf_buffer_poll()
            except KeyboardInterrupt:
                exit()


def main():
    ConnTracer().run()


if __name__ == "__main__":
    main()
