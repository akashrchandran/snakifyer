import os
from rich.console import Console
from rich.emoji import Emoji
from rich.style import Style

from snakifyer.api import Snakify
from .cli import parse_cmd, check_config

snakifyer = Snakify()
console = Console()
config = check_config()
parse_cmd(config)
print(config["email"], config["password"])
snakifyer.login(config["email"], config["password"])
logo = '''
                                                                ++++                                
                                                               ++++++                               
                ++++                                           ++++++                               
             ++++++++++                                        ++ +++                               
        %++++++++++++++                                       +++ +++                               
      +++++++++++++++++                      ++               +++ +++                               
    ++++++++++  ;++                         ++++              ++* +++                               
  ++++++++                                  +++;       +++    +++                                   
 ++++++                                     +++        +;+   +++                                    
+++++                 ;                    *+++        +++   +++              +                     
++++                 +++           ++++    +++               +++++++         +++                    
++++                 +++ ++       +++++++  +++    ++   ;+   +++++++++        +++  +++++      ++     
+++                  +++++++     ++++++++  +++ *+++++  +++++++++++++        ++++ ++++++++    +++++++
+++                  ++++++++   *+++  +++ +++++++++++  +++++++++   ;++      +++ ++++++++++   +++++++
++++;                ++++?+++   +++   +++ +++++++++    +++++++++   +++      +++;+++   +++++  +++++++
+++++++++            ++++ +++  *++;  *++  +++++        +++   +++   +++     +++ ++++++++++++  ++++ ++
 ++++++++++++       +++++ +++  +++   +++  +++++++      +++   +++   ++++    +++ ++++++++++++  +++   +
   +++++++++++++    ++++  ++++ +++   +++  ++++++++     +++   +++   ++++   ;++  +++++++++++*  +++    
        ++++++++++  ++++   +++ +++  ++++; +++  +++++   +++   +++    +++   +++  +++;          +++    
           ++++++++ ++++   +++ +++ ++++++ +++   *++++  +++   +++    ++++  ++*  +++     ;++   +++    
              +++++++++    +++ ++++++++++ +++     ++++ +++   +++     +++ +++   ++++    +++;  +++    
                +++++++    +++;++++++++++ +++      +++++++   +++%    +++++++    ++++  ++++  ;+++    
       +++++++  +++++++    %+++++++++ +++++++       ++++++   ++++     +++++     ;+++++++++  ;+++    
     ++++++++++++++++++     +++ ++++   ++++++          +++    +++     +++++      ++++++++   ++++    
   *++++++++++++++++++                  ++ ++           ++     *+      +++         ++++      ++     
  +++++++++++++++++++            +                                    ++++                          
 ++++++;       ++++++++       ++++                                    +++                           
 ++++        ++++++++++++++++++++                                    ++++                           
 +++       +++++?   +++++++++++                                      ++++                           
 +++    ;++++++                                                      +++                            
 ++++++++++++*                                                      ++++                            
  ++++++++++                                                        +++                             
    +++++                                                           +++                             
                                                                   ++++                             
                                                                   ++++                             
                                                                   ++++                             
'''

def main():
    print(logo, end="\n\n")
    console.print("[bright_green]Welcome to Snakifyer, select one option from below to continue")
    console.print("[bold yellow]1. Solve all problems in a specific section")
    console.print("[bold yellow]2. Solve all problems", end="\n\n")
    choice = console.input("[bold red]Enter your choice: ")
    print()
    if choice == '1':
        sections = snakifyer.get_all_sections()
        console.print("[yellow]" + "\n".join(sections.keys()), end="\n\n")
        choice = list(sections.keys())[int(console.input("[bold red]Enter the choice: ")) - 1]
        problems = snakifyer.get_all_problems_in_section(sections[choice])
    elif choice == '2':
        problems = snakifyer.get_all_problems()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    with console.status("Starting the Interface", spinner_style=Style(color='yellow')) as status:
        for problem in problems:
            status.update(f"[bold yellow]Working on {problem['name']}")
            code = snakifyer.get_code(problem["slug"])
            ans = snakifyer.get_ans(problem["link"])
            if (isinstance(ans, list)):
                result = snakifyer.submit(problem["slug"], code, ans)
            elif (isinstance(ans, str)):
                result = snakifyer.save_progress(problem["slug"], ans)
            if result == 'ok':
                console.print(f"[bold green]{Emoji('white_check_mark')} {problem['name']} complete")
            else:
                console.print(f"[bold green]{Emoji('x')} {problem['name']} errored out")