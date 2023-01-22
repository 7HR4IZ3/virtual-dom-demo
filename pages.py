from virtual_dom import VirtualDom, BaseContext, Reactive, task
import time

class AppContext(BaseContext):
    count = Reactive()
    clock = Reactive()

    def __init__(self):
        super().__init__()
        self.count = 0
        self.clock = time.ctime()
        self.running = True
        self.interval = None
    
    def on_count_change(self, old, new):
        self.browser.document.querySelector('#count').innerHTML = f"Count: {new}"
    
    def on_clock_change(self, old, new):
        self.browser.document.querySelector('#clock').innerHTML = f"Time: {new}"
    
    def create_class(self):
        r = self.browser.Rect.new(7, 9)
        print(r)
        # self.browser.createClass({
        #     "constructor": ""
        # })

    def loaded(self):
        self.browser.alert("Page Loaded.")

    def increment(self):
        self.count += 1

    def reset(self):
        self.browser.alert("Reset")
        self.count = 0

    def get_age(self):
        age = self.browser.prompt("Your age: ")
        self.browser.document.querySelector("#age").innerHTML = f"Your age: {age} years!"

    def check_clock(self):
        self.clock = time.ctime()
        
    def reset_clock(self):
        self.clock = 0

    def pause_clock(self):
        self.browser.clearInterval(self.interval)

    def start_clock(self):
        self.interval = self.browser.js("setInterval(() => {server.check_clock.then(f=>f())}, 1000)")

dom = VirtualDom(context=AppContext)
html = dom.HTML

def generate_page(*a, **kw):
    return html(
        html.head(
            html.script(src="/static/htmlparser.js"),
            html.script(src="/static/html2json.js")
        ),
        html.body(
            html.header(
                html.nav(
                    html.ul(
                        html.li(html.a("Nav item 1", href="/1")),
                        html.li(html.a("Nav item 2", href="/2")),
                        html.li(html.a("Nav item 3", href="/3")),
                        html.li(html.a("Nav item 4", href="/4")),
                    )
                )
            ),
            *a, **kw
        )
    )

clockpage = generate_page(
    html.main(
    	html.h1("Clock"),
        html.div(
            html.p(f"Time: 0", id="clock"),
        ),
        html.section(
            html.button("Start", onclick=dom.context.start_clock),
            html.button("Pause", onclick=dom.context.pause_clock),
            # html.button("Continue", onclick=dom.context.continue_clock),
            # html.button("Create Class", onclick=dom.context.create_class),
        ),
        html.script("""
            class Rect {
                constructor(x, y) {
                    console.log(x,y)
                    this.x = x;
                    this.y = y;
                }
            }
        """)
    )
)

homepage = generate_page(
    html.main(
        html.div(
            html.h2("Hello World"),
            html.p(f"Count: 0", id="count"),
            html.p(id="age"),
            html.button("Increment", onclick=dom.context.increment),
            html.button("Reset", onclick=dom.context.reset),
            html.button("Enter Age", onclick=dom.context.get_age)
        ),
        html.section(
            html.form(
                html.label("Name: "),
                html.input(type="text"),
                html.button("Submit", type="submit")
            )
        )
    )
)
