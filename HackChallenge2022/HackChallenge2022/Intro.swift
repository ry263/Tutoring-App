//
//  SignInController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/6/22.
//

import Foundation
import UIKit

class SignInController: UIViewController {
    
    weak var window: UIWindow?
    weak var user: User?
    var welcome = UILabel()
    var logo = UIImageView()
    var bottomHalf = UIImageView()
    var signLabel = UITextView()
    var signIn = UIButton()
    var logIn = UIButton()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        
        logo.image = UIImage(named: "HCLogo.png")
        logo.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(logo)
        
        bottomHalf.image = UIImage(named: "Color.png")
        bottomHalf.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(bottomHalf)
        
        welcome.text = "Welcome!"
        welcome.font = .systemFont(ofSize: 36)
        welcome.textAlignment = .center
        welcome.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(welcome)
        
        signLabel.text = "Sign in to begin tutoring or get help in a course"
        signLabel.textAlignment = .center
        signLabel.isUserInteractionEnabled = false
        signLabel.font = .systemFont(ofSize: 24)
        signLabel.backgroundColor = UIColor(red: 0.91, green: 0.92, blue: 0.72, alpha: 1.00)
        signLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(signLabel)
        
        signIn.setTitle(" Sign up ", for: .normal)
        signIn.setTitleColor(.black, for: .normal)
        signIn.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        signIn.addTarget(self, action: #selector(SignIn), for: .touchUpInside)
        signIn.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(signIn)
        
        logIn.setTitle(" Log in ", for: .normal)
        logIn.setTitleColor(.black, for: .normal)
        logIn.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        logIn.addTarget(self, action: #selector(LogIn), for: .touchUpInside)
        logIn.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(logIn)
        
        setUpConstraints()
    }
    
    func setUpConstraints() {
        
        NSLayoutConstraint.activate([welcome.centerXAnchor.constraint(equalTo: view.centerXAnchor), welcome.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 60), welcome.bottomAnchor.constraint(equalTo: welcome.topAnchor, constant: 40), welcome.leadingAnchor.constraint(equalTo: welcome.centerXAnchor, constant: -80), welcome.trailingAnchor.constraint(equalTo: welcome.centerXAnchor, constant: 80)])
        
        NSLayoutConstraint.activate([logo.centerXAnchor.constraint(equalTo: view.centerXAnchor), logo.centerYAnchor.constraint(equalTo: welcome.bottomAnchor, constant: 70)])
        
        NSLayoutConstraint.activate([bottomHalf.topAnchor.constraint(equalTo: view.centerYAnchor),bottomHalf.leadingAnchor.constraint(equalTo: view.leadingAnchor),bottomHalf.trailingAnchor.constraint(equalTo: view.trailingAnchor),bottomHalf.bottomAnchor.constraint(equalTo: view.bottomAnchor)])
        
        NSLayoutConstraint.activate([signLabel.topAnchor.constraint(equalTo: bottomHalf.topAnchor, constant: 20), signLabel.bottomAnchor.constraint(equalTo: signLabel.topAnchor, constant: 120),signLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 40), signLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -40)])
        
        NSLayoutConstraint.activate([signIn.topAnchor.constraint(equalTo: signLabel.bottomAnchor, constant: 10),signIn.leadingAnchor.constraint(equalTo: signLabel.leadingAnchor, constant: 30), signIn.trailingAnchor.constraint(equalTo: signLabel.trailingAnchor, constant: -40)])
        
        NSLayoutConstraint.activate([logIn.topAnchor.constraint(equalTo: signIn.bottomAnchor, constant: 10),logIn.leadingAnchor.constraint(equalTo: signLabel.leadingAnchor, constant: 30), logIn.trailingAnchor.constraint(equalTo: signLabel.trailingAnchor, constant: -40)])
        
        
        
    }
    
    @objc func SignIn() {
        let vc = SignUp()
        vc.parentController = self
        vc.emailField.becomeFirstResponder()
        present(vc, animated: true, completion: nil)
    }
    
    @objc func LogIn() {
        let vc = LogOn()
        vc.parentController = self
        vc.emailField.becomeFirstResponder()
        present(vc, animated: true, completion: nil)
    }
}

class LogOn: UIViewController {
    
    weak var parentController: SignInController!
    var emailLabel = UILabel()
    var emailField = UITextField()
    var passLabel = UILabel()
    var passField = UITextField()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        
        emailLabel.text = "Email:"
        emailLabel.font = .systemFont(ofSize: 24)
        emailLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(emailLabel)
        
        emailField.layer.cornerRadius = 10
        emailField.borderStyle = .none
        emailField.delegate = self
        emailField.autocapitalizationType = .none
        emailField.textAlignment = .center
        emailField.backgroundColor = UIColor(red: 0.91, green: 0.92, blue: 0.72, alpha: 1.00)
        emailField.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(emailField)
        
        passField.layer.cornerRadius = 10
        passField.delegate = self
        passField.borderStyle = .none
        passField.autocapitalizationType = .none
        passField.textAlignment = .center
        passField.backgroundColor = UIColor(red: 0.91, green: 0.92, blue: 0.72, alpha: 1.00)
        passField.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(passField)
        
        passLabel.text = "Password:"
        passLabel.font = .systemFont(ofSize: 24)
        passLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(passLabel)
        
        setUpConstraints()
    }
    
    func setUpConstraints() {
        NSLayoutConstraint.activate([emailLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor,constant: 40), emailLabel.bottomAnchor.constraint(equalTo: emailLabel.topAnchor, constant: 40), emailLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor,constant: 40),emailLabel.trailingAnchor.constraint(equalTo: emailLabel.leadingAnchor, constant: 120)])
        
        NSLayoutConstraint.activate([emailField.topAnchor.constraint(equalTo: emailLabel.bottomAnchor, constant: 20), emailField.bottomAnchor.constraint(equalTo: emailField.topAnchor, constant: 40), emailField.leadingAnchor.constraint(equalTo: emailLabel.leadingAnchor), emailField.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -40)])
        
        NSLayoutConstraint.activate([passLabel.topAnchor.constraint(equalTo: emailField.bottomAnchor, constant: 20), passLabel.bottomAnchor.constraint(equalTo: passLabel.topAnchor, constant: 40), passLabel.leadingAnchor.constraint(equalTo: emailLabel.leadingAnchor), passLabel.trailingAnchor.constraint(equalTo: emailLabel.trailingAnchor)])
        
        NSLayoutConstraint.activate([passField.topAnchor.constraint(equalTo: passLabel.bottomAnchor,constant: 20), passField.bottomAnchor.constraint(equalTo: passField.topAnchor, constant: 40), passField.leadingAnchor.constraint(equalTo: emailField.leadingAnchor), passField.trailingAnchor.constraint(equalTo: emailField.trailingAnchor)])
    }
    
    func showAlert() {
        let alert = UIAlertController(title: "Invalid input", message: "Incorrect Login", preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: "Ok", style: .cancel) { _ in })
        
        present(alert, animated: true,completion: nil)
    }
}

extension LogOn: UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        
        if textField.isEqual(self.emailField) {
            self.passField.becomeFirstResponder()
        }
        if textField.isEqual(self.passField) {
            if emailField.text != nil && emailField.text != "" {
                if passField.text != nil && passField.text != "" {
                    NetworkManager.LogIn(email: emailField.text!, password: passField.text!) { User in
                        self.parentController.user = User
                        let vc = TabBar()
                        vc.user = self.parentController.user
                        vc.setUpTabBar()
                        self.parentController.window?.rootViewController = vc
                        return
                    }
                    showAlert()
                    return
                }
                showAlert()
                return
            }
            showAlert()
            return
        }
    }
}

class SignUp: UIViewController {
    
    weak var parentController: SignInController!
    var emailLabel = UILabel()
    var emailField = UITextField()
    var passLabel = UILabel()
    var passField = UITextField()
    var nameLabel = UILabel()
    var nameField = UITextField()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 0.72, green: 0.82, blue: 0.92, alpha: 1.00)
        
        emailLabel.text = "Email:"
        emailLabel.font = .systemFont(ofSize: 24)
        emailLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(emailLabel)
        
        emailField.layer.cornerRadius = 10
        emailField.delegate = self
        emailField.borderStyle = .none
        emailField.autocapitalizationType = .none
        emailField.textAlignment = .center
        emailField.backgroundColor = UIColor(red: 0.91, green: 0.92, blue: 0.72, alpha: 1.00)
        emailField.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(emailField)
        
        passField.layer.cornerRadius = 10
        passField.delegate = self
        passField.borderStyle = .none
        passField.autocapitalizationType = .none
        passField.textAlignment = .center
        passField.backgroundColor = UIColor(red: 0.91, green: 0.92, blue: 0.72, alpha: 1.00)
        passField.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(passField)
        
        passLabel.text = "Password:"
        passLabel.font = .systemFont(ofSize: 24)
        passLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(passLabel)
        
        nameLabel.text = "Name:"
        nameLabel.font = .systemFont(ofSize: 24)
        nameLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(nameLabel)
        
        nameField.layer.cornerRadius = 10
        nameField.delegate = self
        nameField.textAlignment = .center
        nameField.autocapitalizationType = .none
        nameField.backgroundColor = UIColor(red: 0.91, green: 0.92, blue: 0.72, alpha: 1.00)
        nameField.borderStyle = .none
        nameField.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(nameField)
        
        setUpConstraints()
    }
    
    func setUpConstraints() {
        NSLayoutConstraint.activate([emailLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor,constant: 40), emailLabel.bottomAnchor.constraint(equalTo: emailLabel.topAnchor, constant: 40), emailLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor,constant: 40),emailLabel.trailingAnchor.constraint(equalTo: emailLabel.leadingAnchor, constant: 120)])
        
        NSLayoutConstraint.activate([emailField.topAnchor.constraint(equalTo: emailLabel.bottomAnchor, constant: 20), emailField.bottomAnchor.constraint(equalTo: emailField.topAnchor, constant: 40), emailField.leadingAnchor.constraint(equalTo: emailLabel.leadingAnchor), emailField.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -40)])
        
        NSLayoutConstraint.activate([passLabel.topAnchor.constraint(equalTo: emailField.bottomAnchor, constant: 20), passLabel.bottomAnchor.constraint(equalTo: passLabel.topAnchor, constant: 40), passLabel.leadingAnchor.constraint(equalTo: emailLabel.leadingAnchor), passLabel.trailingAnchor.constraint(equalTo: emailLabel.trailingAnchor)])
        
        NSLayoutConstraint.activate([passField.topAnchor.constraint(equalTo: passLabel.bottomAnchor,constant: 20), passField.bottomAnchor.constraint(equalTo: passField.topAnchor, constant: 40), passField.leadingAnchor.constraint(equalTo: emailField.leadingAnchor), passField.trailingAnchor.constraint(equalTo: emailField.trailingAnchor)])
        
        NSLayoutConstraint.activate([nameLabel.topAnchor.constraint(equalTo: passField.bottomAnchor, constant: 20), nameLabel.bottomAnchor.constraint(equalTo: nameLabel.topAnchor, constant: 40), nameLabel.leadingAnchor.constraint(equalTo: emailLabel.leadingAnchor),nameLabel.trailingAnchor.constraint(equalTo: emailLabel.trailingAnchor)])
        
        NSLayoutConstraint.activate([nameField.topAnchor.constraint(equalTo: nameLabel.bottomAnchor,constant: 20), nameField.bottomAnchor.constraint(equalTo: nameField.topAnchor, constant: 40), nameField.leadingAnchor.constraint(equalTo: emailField.leadingAnchor), nameField.trailingAnchor.constraint(equalTo: emailField.trailingAnchor)])
    }
    
    func showAlert() {
        let alert = UIAlertController(title: "Invalid input", message: "Invalid information", preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: "Ok", style: .cancel) { _ in })
        
        present(alert, animated: true,completion: nil)
    }
}

extension SignUp: UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        if textField.isEqual(emailField) {
            passField.becomeFirstResponder()
        } else if textField.isEqual(passField) {
            nameField.becomeFirstResponder()
        } else {
            let array = [self.emailField,self.passField,self.nameField]
            for field in array {
                if field.text == nil || field.text == ""{
                    showAlert()
                    return
                }
            
            
            }
            
            let whitespaceCharacterSet = CharacterSet.whitespaces
            
            for field in array {
                field.text = field.text!.trimmingCharacters(in: whitespaceCharacterSet)
            }

            NetworkManager.registerUser(email: emailField.text!, password: passField.text!, name: nameField.text!, profile_pic: "profile.png") { User in

                self.parentController.user = User
                let vc = TabBar()
                vc.user = self.parentController.user
                vc.setUpTabBar()
                self.parentController.window?.rootViewController = vc
                
            }

            //MARK: Register User with fields and default profile pic
        }
    }
}
    
    
