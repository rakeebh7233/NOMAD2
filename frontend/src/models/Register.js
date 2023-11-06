import "../styles/Register.css";

function Register() {
    return (
        <section class="text-center text-lg-start">
          <div class="container py-4">
            <div class="row g-0 align-items-center">
              <div class="col-lg-6 mb-5 mb-lg-0">
                <div class="card cascading-right" >
                  <div class="card-body p-5 shadow-5 text-center">
                    <h2 class="fw-bold mb-5">Sign up now</h2>
                    <form>
                      {/* <!-- 2 column grid layout with text inputs for the first and last names --> */}
                      <div class="row">
                        <div class="col-md-6 mb-4">
                          <div class="form-outline">
                            <input type="text" id="form3Example1" class="form-control" />
                            <label class="form-label" for="form3Example1">First name</label>
                          </div>
                        </div>
                        <div class="col-md-6 mb-4">
                          <div class="form-outline">
                            <input type="text" id="form3Example2" class="form-control" />
                            <label class="form-label" for="form3Example2">Last name</label>
                          </div>
                        </div>
                      </div>
        
                      <div class="form-outline mb-4">
                        <input type="email" id="form3Example3" class="form-control" />
                        <label class="form-label" for="form3Example3">Email address</label>
                      </div>
        
                      <div class="form-outline mb-4">
                        <input type="password" id="form3Example4" class="form-control" />
                        <label class="form-label" for="form3Example4">Password</label>
                      </div>
        
                      <button type="submit" class="btn btn-primary btn-block mb-4">
                        Sign up
                      </button>
        
                      <div class="text-center">
                        <p>or sign up with:</p>
                        <button type="button" class="btn btn-link btn-floating mx-1">
                          <i class="fab fa-facebook-f"></i>
                        </button>
        
                        <button type="button" class="btn btn-link btn-floating mx-1">
                          <i class="fab fa-google"></i>
                        </button>
        
                        <button type="button" class="btn btn-link btn-floating mx-1">
                          <i class="fab fa-twitter"></i>
                        </button>
        
                        <button type="button" class="btn btn-link btn-floating mx-1">
                          <i class="fab fa-github"></i>
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
        
              <div class="col-lg-6 mb-5 mb-lg-0">
                <img src="https://images.unsplash.com/photo-1500835556837-99ac94a94552?auto=format&fit=crop&q=80&w=1887&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" class="w-100 rounded-4 shadow-4" height="625" />
              </div>
            </div>
          </div>
        </section>
    )
}

export default Register;