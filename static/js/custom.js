function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function unescapeHTML(text) {
    const div = document.createElement('div');
    div.innerHTML = text;
    return div.textContent??"";
}

const fetchUserInfo = async (username) => {
    const response = await fetch(`https://api.github.com/users/${username}`);
    if (response.ok) {
        const data = await response.json();
        document.querySelector('.github-avatar').src = data.avatar_url;
        document.querySelector('.github-name').innerText = data.name;
        document.querySelector('.github-username').innerText = data.login;
        document.querySelector('.github-brief').innerText = data.bio;
        // document.querySelector('.github-location').innerText = data.location;
        // document.querySelector('.github-url').href = data.html_url;
        // document.querySelector('.github-url').innerText = data.html_url;
    }
}

const generateSummary = () => {
    // 注意：数值越小级别越高
    const levels = { H1: 1, H2: 2, H3: 3, H4: 4, H5: 5, H6: 6, };
    const summary = document.querySelector(".summary");
    const markdown = document.querySelector("#article-content");
    const headings = markdown.querySelectorAll("h1,h2,h3,h4,h5,h6");
    summary.innerHTML = ""

    // 生成树
    let forest = []; // 一级标题，可能有多个
    let stack = [];
    const range = [-1, 300]; // 坐标为浮点数，滚动存在浮点误差，使用 -1 做冗余
    let focused = false;
    for (let i = 0; i < headings.length; i++) {
        const heading = headings[i];
        heading.id = unescapeHTML(heading.innerText).replace(/\s+/g, "-");
        const level = levels[(heading.tagName)]
        const currentY = heading.getBoundingClientRect().y;
        const nextY = i + 1 < headings.length ? headings[i + 1].getBoundingClientRect().y : document.body.clientHeight;
        const node = {level: level, text: heading.innerText, refer:heading, focus: false, children: []};

        if (!focused && currentY >= range[0] && currentY <= range[1]) {
            node.focus = true;
            focused = true
        } else if (!focused && currentY < range[0] && nextY > range[1]) {
            node.focus = true;
            focused = true
        }

        // 如果栈顶结点的级别不高于当前节点，则出栈，向前查找父节点
        while (stack.length > 0 && stack[stack.length - 1].level >= level) {
            stack.pop();
        }
    
        if (stack.length === 0) {
            // 如果栈为空，说明这是最顶层的节点（），作为树的根节点加入森林
            forest.push(node);
        } else {
            // 否则，将该节点作为栈顶元素的子节点
            stack[stack.length - 1].children.push(node);
        }
    
        // 将当前节点压入栈中，处理下一个标题
        stack.push(node);
    }

    // 节点生成函数
    const generateSummaryNode = (node) => {
        const element = document.createElement("li");
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = node.focus ? "btn btn-link text-success" : "btn btn-link link-secondary";
        btn.style = "padding:0;";
        btn.innerText = node.text;
        btn.onclick = () => {node.refer.scrollIntoView()}
        element.appendChild(btn);
        if (node.children.length > 0) {
            const sub = document.createElement("ol");
            for (const subnode of node.children) {
                sub.appendChild(generateSummaryNode(subnode));
            }
            element.appendChild(sub);
        }
        return element;
    }

    // 生成目录
    for (const tree of forest) {
        const element = generateSummaryNode(tree);
        summary.appendChild(element);
    }
}

function debounce(fn, ms = 100) {
    let timerId;

    return () => {
        clearTimeout(timerId);
        timerId = setTimeout(fn, ms);
    }
}

function dynamicSummary() {
    const fn = debounce(generateSummary);
    fn();
    window.addEventListener("scroll", fn);
}

function scanTime() {
    const elements = document.querySelectorAll(".time");
    for (element of elements) {
        const t = new Date(element.innerText);
        element.innerText = t.toLocaleString();
    }
}