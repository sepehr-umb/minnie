import './App.css'
import AboutMe from './components/AboutMe'

function App() {
  return (
    <>
      <section id="center">
        <div className="hero">
          {/* <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" /> */}
        </div>
        <div>
          <h1>Project Explore Minnie</h1>
        </div>
      </section>

      <div className="ticks"></div>

      <section id="next-steps">
        <div id="docs">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="icons.svg#documentation-icon"></use>
          </svg>
          <h2>Documentation</h2>
          <p>Your questions, answered</p>
          <ul>
            <li>
              <a href="https://github.com/B8ExploreM/Explore-Minnie/blob/frontend/frontend/README.md" target="_blank">
                <img className="button-icon"/>
                Learn more
              </a>
            </li>
          </ul>
        </div>
        <div id="social">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="icons.svg#social-icon"></use>
          </svg>
          <h2>Connect with us</h2>
          <p>View our work</p>
          <ul>
            <li>
              <a href="https://github.com/B8ExploreM/Explore-Minnie" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="icons.svg#github-icon"></use>
                </svg>
                GitHub
              </a>
            </li>
          </ul>
        </div>
      </section>
      <div className="ticks"></div>
      <section id="spacer">
      <AboutMe/>
      </section>
    </>
  )
}

export default App
