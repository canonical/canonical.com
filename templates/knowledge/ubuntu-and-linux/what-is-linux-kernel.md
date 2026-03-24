---
wrapper_template: "knowledge/_base_knowledge_markdown.html"
context:
  category: "Ubuntu and Linux"
  title: "What is the Linux Kernel? | Ubuntu and Linux | Linux kernel"
  breadcrumb: "What is the Linux Kernel?"
  copydoc: "https://docs.google.com/document/d/12SqjuRNZl-Ho8AZ80nd1JONgtgPeigKyjYhWuwfAscI/edit?tab=t.0#heading=h.yeo17q3utlgo"
  hero_title: "What is the Linux Kernel?"
  cta:
    description: "Curious about Linux? You might want to read our articles about the available Linux variants, the importance of maintenance and why developers add their own patches to customize the kernel or the kernel release cycle."
    buttons:
      - text: "View the codebase"
        url: "https://github.com/torvalds/linux"
        type: "button"
        variant: "positive"
      - text: "Read the documentation"
        url: "https://www.kernel.org/doc/html/latest/"
        type: "button"
  blog:
    id: 1364
---
{% from "macros/_macros-text-list.jinja" import text_list_kh %}
{% from "macros/_macros-image.jinja" import image_kh %}
{% from "macros/_macros-lite-video.jinja" import lite_video %}

The Linux kernel is widely used and its codebase ever-increasing, so it can feel daunting for a newcomer to wrap their head around it. This article aims to make the fascinating world of Linux feel less intimidating. Linux for human beings, you might say.

## What is the history of Linux?

### Linux has its roots in Unix

One cannot mention the rise of Linux without a reference to its “precursor”, Unix.

Unix emerged as a successor to the[ Multics](https://en.wikipedia.org/wiki/Multics#) project, an ambitious but ultimately unsuccessful attempt to create a multi-user operating system. At Bell Labs in 1969, Multics developers Ken Thompson and Dennis Ritchie [began their journey](https://www.scs.stanford.edu/nyu/04fa/sched/readings/unix.pdf) by drafting a new filesystem design that ultimately became the foundation of Unix.

Unix's early appeal lay in its simplicity and the fact that its source code was distributed openly, which encouraged outside institutions to experiment and expand on it. Among these, the University of California, Berkeley, played a pivotal role, and its contributions gave rise to the [Berkeley Software Distributions (BSD)](https://www.gnu.org/licenses/license-list.html#OriginalBSD). Because BSD was released under a permissive license allowing users to freely use, modify, and distribute the software, even for commercial purposes, its legacy lives on in projects such as [FreeBSD](https://www.freebsd.org/), [NetBSD](https://www.netbsd.org/), and [OpenBSD](https://www.openbsd.org/).

During the 1980s and 1990s, many workstation and server vendors launched their own commercial Unix versions, typically based on AT&T’s or Berkeley’s codebase. Several factors explain Unix’s success. First, it embraced simplicity: where other systems offered thousands of system calls with complex design goals, Unix provided only a few hundred, organized around a clear and minimalist architecture. Second, it aimed to make everything a file, which unified the handling of data and devices under a small set of core operations.

Modern Unix systems are highly capable. They introduced [preemptive multitasking](https://ubuntu.com/blog/real-time-kernel-technical), where the operating system can interrupt tasks to give other tasks a fair share of CPU time; [multithreading](https://documentation.ubuntu.com/real-time/latest/explanation/schedulers/), which allows a program to split into multiple parallel tasks; shared libraries with on-demand loading, loading parts of a program into memory only when needed;  [virtual memory](https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html); demand paging,  and TCP/IP networking. Variants range from those running on small embedded hardware to versions scaling across hundreds of processors. If Unix was quite successful in its own right, what was the need to develop Linux, then?

{{ image_kh(url="https://assets.ubuntu.com/v1/a91e18ef-image_container.png",
  alt="",
  width="1200",
  height="500",
  hi_def=True,
  loading="lazy"
  ) | safe
}}

### Who is Linus Torvalds?

*I'm doing a (free) operating system (just a hobby, won't be big and professional like gnu) for 386(486) AT clones.  [...] It is NOT portable (uses 386 task switching etc), and it probably never will support anything other than AT-harddisks, as that's all I have :-(.”*

\- Linus Torvalds’ [announcement](https://groups.google.com/g/comp.os.minix/c/dlNtH7RRrGA/m/SwRavCzVE7gJ) of Linux

In 1991, Linus Torvalds, then a student at the University of Helsinki, created Linux, initially targeting Intel’s 80386 processor. Although he had previously used [Minix](https://www.minix3.org/), a teaching-oriented Unix-like system, he was frustrated by the restrictions its license placed on modifying and redistributing source code. This led him to start his own kernel, which quickly grew into a collaborative, community-driven project.

{{ image_kh(url="https://assets.ubuntu.com/v1/f370aaaa-image_wrapper.png",
  alt="",
  width="1200",
  height="500",
  hi_def=True,
  loading="lazy",
  caption="Intel 80386 processor, supported by the Linux kernel <a href='https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=743aa456c1834f76982af44e8b71d1a0b2a82e21'>until</a> 2012"
  ) | safe
}}

While Linux draws heavily on Unix ideas and implements its APIs (Application Programming Interfaces),* *which are the set of rules and function calls that programs use to request services from the OS, it is not derived from the original Unix source. Instead, it represents an independent implementation that, while occasionally diverging from traditional approaches, has stayed true to Unix’s design principles and maintained compatibility with standardized application interfaces.

Now that we know a bit more about the history of Linux, let’s look into what makes it so special, starting with the basics.

## The basics of the Linux kernel

The Linux kernel is released as free and open-source software under the [GNU General Public License (GPL) version 2](https://github.com/torvalds/linux?tab=License-1-ov-file#readme). This license allows anyone to download, study, and modify the kernel’s source code. The only requirement is that if modified versions are shared, they must also remain under the same license, ensuring continued access to the source and the same freedoms for others.

While that all makes sense, why would a developer want to modify the kernel in the first place? 

### Does “Linux” refer to the kernel or the OS?

Strictly speaking, the word “Linux” refers only to the kernel itself, as a complete Linux operating system (OS) typically includes several other essential components. Among those are a C standard library, a compiler toolchain, and core system utilities, such as the login manager and shell. In practice, a Linux system encompasses all the elements necessary for basic operation and administration.

But let’s not get ahead of ourselves. For now, we’ll focus just on the core of the OS: the kernel proper.


### What is a kernel?

The kernel forms the foundation of the system. It provides the essential services which all other software relies on, manages hardware, and allocates system resources. Common components inside the kernel include interrupt handlers to respond to hardware signals, a scheduler to divide CPU time among processes, memory management for handling process address spaces, and core services such as networking and interprocess communication.

A key concept within the Linux kernel world is “where” processes run. A processor, often called a CPU, is the hardware unit in a computer that carries out instructions, fetching them from memory, performing calculations, and moving data around.

Modern microprocessors support code execution at a minimum of two privilege levels, hardware-enforced execution tiers that restrict what operations code is allowed to perform. . For instance, Intel and AMD processor families support four ring levels, arm32 microprocessors support seven execution modes, and so on. The kernel's Virtual Address Space (VAS), the range of virtual memory addresses visible to and managed by the system, is then "split" into at least clearly distinguished (virtual) address spaces. A processor is always engaged in one of three areas:

{{ text_list_kh(
  type="number",
  items=[
  "User-space, running code as part of an application process. This is for applications like email clients and browsers to run in unprivileged mode",
  "Kernel space, within the context of a process, executing on that process's behalf. This is for the kernel and all its components to run in privileged mode",
  "Kernel space outside of any process context, handling interrupts triggered by hardware."
]) }}

{{ image_kh(url="https://assets.ubuntu.com/v1/f3503425-image_container_1.png",
  alt="",
  width="1200",
  height="800",
  hi_def=True,
  loading="lazy",
  caption="Sketch based on drawing in <a href='https://rlove.org/'>Robert Love’s Linux kernel development</a>"
  ) | safe
}}

### Defining kernel and user space

What are the kernel and user space? Simplifying, they’re two different “worlds” inside your computer. It helps to think about safety and control. An OS needs a protected area where it can directly manage hardware and memory without interference from applications. That protected area is kernel space. The kernel’s world has full control of the machine: it can talk directly to the CPU, memory, and devices. Everything else lives in user space, where access is limited to prevent accidents or malicious behaviour.  The user’s world is where everyday programs live, carefully protected so they can’t accidentally crash the whole system.

It follows from the above that the kernel operates in a privileged state distinct from ordinary user programs. This privileged environment has unrestricted access to hardware and protected memory regions. By contrast, applications run in user space, where access is limited and controlled. This separation ensures that user processes cannot directly manipulate hardware or interfere with other processes’ memory. 

When the system executes kernel code, it runs in kernel mode, while ordinary applications run in user mode. Applications interact with the kernel through system calls. Typically, programs do not invoke system calls directly. Instead, they use functions provided by libraries such as the C library, which internally rely on the system call interface to request kernel-level operations.

The kernel also manages hardware communication. Devices notify the system of events by generating interrupts, which temporarily halt the processor’s current task so the kernel can respond appropriately.


### What are the key components of kernel space?

Now that we have a sense of what the kernel is and why it matters, it’s worth taking a closer look at what actually lives inside it. Although the Linux kernel can feel intimidating at first glance, we can understand it as a collection of a few major subsystems working together. Each one takes responsibility for a core part of the overall behaviour. Let’s walk through the most important pieces.


{{ image_kh(url="https://assets.ubuntu.com/v1/34745594-image_container2.png",
  alt="",
  width="1200",
  height="800",
  hi_def=True,
  loading="lazy",
  caption="Major subsystems of the Linux kernel based on Kaiwan Billimoria's <a href='https://www.packtpub.com/en-us/product/linux-kernel-programming-9781789953435'>Linux Kernel Programming</a>"
  ) | safe
}}


#### Core kernel

 At the heart of everything is the core kernel. This is the machinery that keeps the system running. This is where the kernel decides which process gets CPU time next, how threads are created and cleaned up, and how the system responds when hardware interrupts demand immediate attention. It also provides the fundamental building blocks used elsewhere in the kernel, like synchronization primitives, timers, system call handling and more.


#### Memory management 

The memory management subsystem is responsible for creating and maintaining virtual address spaces for both the kernel and every running process. As you can imagine, memory is one of the most precious resources in any computer, and Linux treats it accordingly. It handles everything from page faults and caching to physical memory allocation and interaction with the hardware MM Unit.


#### Virtual Filesystem Switch (VFS) 

The VFS is how Linux abstracts the world of filesystems. Application developers don't need to worry about the differences between different filesystems, like ext4, XFS or Btrfs. Instead, the VFS in the kernel provides one unified view and defines a common set of operations like open, read, write and rename, that each specific filesystem then implements in its own way.


#### Block I/O 

The block layer handles storage hardware. It manages queues, schedules I/O, merges requests, and hands work off to block device drivers. When a filesystem issues a read or write, for instance, the block layer turns the request into disk operations.


#### Networking subsystem 

The Linux kernel’s networking subsystem handles all network communication. It is a full-fledged implementation to process packets, handle routing, manage TCP/IP connections, enforce firewall rules, and talk to network device drivers. Everything we commonly do online, from loading a webpage to connecting over SSH, is enabled by this part of the kernel. 


## How does Linux handle inter-process communication (IPC)?

Inter-process communication refers to processes coordinating with each other and safely exchanging data. Linux provides several ways for programs to communicate, including message queues, shared memory, semaphores, pipes and UNIX domain sockets.


### Sound subsystem

Audio on Linux is handled by the sound subsystem, which manages audio device drivers, mixing, sampling, MIDI streams, and low-latency playback. Whether you’re listening to a recording or running real-time audio processing code on Linux, this subsystem ensures the data gets where it needs to go.


### Virtualization support 

Through the Kernel-based Virtual Machine (KVM), the kernel can act as a hypervisor, using hardware virtualisation extensions to run virtual machines. Linux is known for treating virtualized environments as “first-class citizens”, meaning that VMs are treated with the same importance, ease, and support as other core components within Linux. 


## How do userspace processes communicate with the kernel?

User space and kernel space occupy separate virtual address spaces and operate at different privilege levels. Because of this separation, user applications cannot directly execute privileged operations or access kernel-managed resources. Instead, the only way for a user-space process or thread to request services from the kernel is through system calls, a specialised, well-defined API exposed by the kernel itself.

User-space applications, however, do not interact with the kernel solely through direct system calls. Often,  they rely on library APIs, which are standardised, well-written, and well-tested interfaces such as the C standard library glibc, POSIX libraries, or domain-specific libraries. A library is essentially a collection or archive of APIs which abstract away the underlying system calls and provide higher-level, portable functions. For example, printf(), fopen(), or pthread_create() are library APIs that translate into system calls like write(), open(), or clone(), but with additional logic, error handling, and convenience.


## How can kernel code execute?

To understand how Linux operates, it helps to see *when* the kernel actually executes. Although the kernel is large, all of its code runs in just two situations, known as “contexts”. Whether responding to a system call or reacting to hardware, all kernel execution falls into one of these two contexts. Linux switches into kernel mode to do its work and then returns control when it’s safe to do so.


### Process context

 Most entry points into the kernel come from user space. When a process or thread makes a system call, the CPU switches from user mode to privileged kernel mode. The same process continues running, but it is now executing in kernel code. In this context, the kernel is working "on behalf" of the calling process, as it can access the process’s memory, perform blocking operations, or return data to user space. Even certain exceptions, like page faults, follow this same pattern. The CPU catches into the kernel, the kernel handles the issue, and execution resumes in the same process.


### Interrupt context

The other way kernel code runs is when hardware interrupts demand immediate attention. A device like a network card, a disk controller, or a timer triggers an interrupt, causing the CPU to pause its current work, save the process’s state, and jump into an interrupt handler. This code does *not* run for any specific process and cannot block or sleep. It is asynchronous and often time-critical, essentially forming the kernel’s reaction layer to external events.

{{ lite_video(video_id="1eqEpf9hPKk", video_title="Starting Your Career at Canonical - Journey to Prof I") | safe }}

## Ubuntu and the Linux kernel

There's so much more that can be said about each of the themes we touched upon so far. But we’ve already covered a lot of ground!

We learnt that Linux traces its roots to Unix, developed at Bell Labs in 1969, valued for its simplicity and open distribution. In 1991, Linus Torvalds created Linux as a free, community-driven kernel, independent of Unix’s source but inspired by its principles. Released under the GNU GPLv2, Linux allows anyone to study, modify, and redistribute its code. The kernel forms the system’s core, managing processes, memory, hardware, networking, and communication between applications and devices. A central concept is the split between kernel space for privileged operations and user space for applications, with interactions handled through system calls. This separation makes Linux a powerful, flexible, and central component of countless modern systems.

Ubuntu builds on this rich legacy. By packaging the Linux kernel together with essential tools, libraries, and a consistent user experience, Ubuntu makes that power accessible to individuals, businesses, and developers worldwide. In doing so, we stand on the shoulders of giants: from Unix pioneers at Bell Labs, to Linus Torvalds and the global Linux community, to the many open-source contributors who continue to shape the ecosystem today.