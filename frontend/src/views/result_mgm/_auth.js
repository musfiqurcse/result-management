const checkAuth = (role)=> {
    const is_superuser = Vue.$cookies.get('is_superuser')
    const is_teacher = Vue.$cookies.get('is_teacher')
    const is_student = Vue.$cookies.get('is_student')
    console.log(Vue.$cookies.get('is_superuser'))
    console.log(typeof(is_superuser))
    console.log('test')
    if(is_superuser === "true" && role === "admin"){
      console.log('prothom-alo')
      return true
    }
    else if(is_teacher === "true" && role === "teacher"){
      console.log('prothom-alo1')
      return true
    }
    else if(is_student === "true" && role === "student"){
      console.log('prothom-alo2')
      return true
    }
    return false
  }
  
  
  export default checkAuth