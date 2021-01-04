import os
import re
import json
from lxml import etree

from multiprocessing import Process, Pool, Manager, Queue

parser = etree.HTMLParser()


def parse(pid, path):
    pi = {}
    pi["pid"] = pid

    tree = etree.parse(path, parser)

    if "Prime Video" in tree.xpath("//title/text()")[0]:
        ## Title
        pi["title"] = tree.xpath('//h1[@data-automation-id="title"]/text()')[0]

        ## keywords
        # may contains category
        pi["keywords"] = [
            keyword.strip()
            for keyword in tree.xpath('//meta[@name="keywords"]/@content')[0].split(",")
        ]

        ## runtime
        pi["runtime"] = tree.xpath(
            '//span[@data-automation-id="runtime-badge"]/text()'
        )[0]

        ## meta-info
        dts = tree.xpath('//div[@id="meta-info"]/div/dl')
        for dt in dts:
            key = "".join(dt.xpath("./dt/span/text()"))
            value = "".join(dt.xpath("./dd//text()"))
            pi[key] = value

        ## more details
        mdts = tree.xpath('//div[@id="btf-product-details"]/div/dl')
        for dt in mdts:
            key = "".join(dt.xpath("./dt/span/text()"))
            value = "".join(dt.xpath("./dd//text()")).replace("more…", "")
            pi[key] = value

        ## otherFormats
        otherFormats = tree.xpath(
            '//div[@data-automation-id="other-formats"]/div/a/@href'
        )
        pi["otherFormat"] = [
            re.search("/dp/(\w+)/", otherFormat).group(1)
            for otherFormat in otherFormats
        ]

    else:
        ## Title
        pi["title"] = tree.xpath('//span[@id="productTitle"]/text()')[0].strip()

        ## keywords
        # may contains category
        pi["keywords"] = [
            keyword.strip()
            for keyword in tree.xpath('//meta[@name="keywords"]/@content')[0].split(",")
        ]

        ## details
        mdts = tree.xpath(
            '//div[@id="detailBullets_feature_div"]/ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]//span[@class="a-list-item"]'
        )
        for dt in mdts:
            key = dt.xpath("./span[1]/text()")[0].strip(" :\r\n\t")
            value = dt.xpath("./span[2]/text()")[0].strip()
            pi[key] = value

        ## format
        pi["format"] = tree.xpath('//div[@id="bylineInfo"]/span[last()]/text()')[0]

        ## otherFormats
        otherFormats = tree.xpath(
            '//div[@id="tmmSwatches"]//li[@class="swatchElement unselected"]//a/@href'
        )
        pi["otherFormat"] = [
            re.search("/dp/(\w+)/", otherFormat).group(1)
            for otherFormat in otherFormats
        ]

        ## additionalOptions
        # Attention: "top-level unselected-row"有两层
        additionalOptions = tree.xpath(
            '//div[@id="twister"]//div[@class="top-level unselected-row"]/span/@data-tmm-see-more-editions-click'
        )
        pi["additionalOptions"] = [
            re.search("/dp/(\w+)/", additionalOption).group(1)
            for additionalOption in additionalOptions
        ]
    return pi


def worker(index, queue):
    print(f"Worker {index} start.")

    with open(f"{index}.jl", "a") as out, open(f"{index}.log", "a") as log, open(
        f"{index}.err", "a"
    ) as err:
        while True:
            pid, path = queue.get(True)
            print(f"Get {pid}")
            try:
                pi = parse(pid, path)
                out.write(json.dumps(pi) + "\n")
                log.write(pid + "\n")
            except Exception as e:
                err.write(f"{pid} {e}\n")
            except KeyboardInterrupt:
                # out.flush()
                # log.flush()
                # err.flush()
                print(f"Stoping worker {index}...")
                break
            queue.task_done()


def init():
    if not os.path.exists("first_run"):
        for i in range(os.cpu_count()):
            if os.path.exists(f"{i}.log"):
                os.remove(f"{i}.log")
            if os.path.exists(f"{i}.err"):
                os.remove(f"{i}.err")
            if os.path.exists(f"{i}.jl"):
                os.remove(f"{i}.jl")

        with open("task.txt", "w") as fp:
            for p, d, f in os.walk("D:\360\html"):
                for _f in f:
                    pid = _f[-16:-6]
                    fp.write(pid + " " + os.path.join(p, _f) + "\n")
        open("first_run", "w").close()

    finished = []
    tasks = []

    for i in range(count):
        if os.path.exists(f"{i}.log"):
            with open(f"{i}.log") as log:
                for line in log:
                    finished.append(line.strip())

    with open("task.txt") as task:
        for line in task:
            line = line.split()
            pid = line[0]
            p = line[1]

            if pid not in finished:
                tasks.append((pid, p))

    return tasks


if __name__ == "__main__":
    count = os.cpu_count()
    print(f"Process: {count}")

    tasks = init()
    print(f"Get tasks: {len(tasks)}")

    with Manager() as manager:
        queue = manager.Queue()
        pool = Pool(count)

        for i in range(count):
            pool.apply_async(worker, (i, queue))
        pool.close()

        for task in tasks:
            queue.put(task)
        print(f"Queue finished")

        pool.join()
        print("All finished.")

