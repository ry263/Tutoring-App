//
//  SignInController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/6/22.
//

import Foundation
import UIKit
import GoogleSignIn

class SignInController: UIViewController {
    
    weak var window: UIWindow?
    var welcome = UILabel()
    var logo = UIImageView()
    var bottomHalf = UIImageView()
    var signLabel = UITextView()
    
    var signIn = GIDSignInButton()
    let signInConfig = GIDConfiguration.init(clientID: "145626881546-hnvg8v87bavj907s65e7hev9pdaeocta.apps.googleusercontent.com")
    var googleSignIn = GIDSignIn.sharedInstance
    
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
        
        signIn.style = .wide
        signIn.addTarget(self, action: #selector(LogIn), for: .touchUpInside)
        signIn.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(signIn)
        
        setUpConstraints()
    }
    
    func setUpConstraints() {
        
        NSLayoutConstraint.activate([welcome.centerXAnchor.constraint(equalTo: view.centerXAnchor), welcome.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 60), welcome.bottomAnchor.constraint(equalTo: welcome.topAnchor, constant: 40), welcome.leadingAnchor.constraint(equalTo: welcome.centerXAnchor, constant: -80), welcome.trailingAnchor.constraint(equalTo: welcome.centerXAnchor, constant: 80)])
        
        NSLayoutConstraint.activate([logo.centerXAnchor.constraint(equalTo: view.centerXAnchor), logo.centerYAnchor.constraint(equalTo: welcome.bottomAnchor, constant: 70)])
        
        NSLayoutConstraint.activate([bottomHalf.topAnchor.constraint(equalTo: view.centerYAnchor),bottomHalf.leadingAnchor.constraint(equalTo: view.leadingAnchor),bottomHalf.trailingAnchor.constraint(equalTo: view.trailingAnchor),bottomHalf.bottomAnchor.constraint(equalTo: view.bottomAnchor)])
        
        NSLayoutConstraint.activate([signLabel.topAnchor.constraint(equalTo: bottomHalf.topAnchor, constant: 20), signLabel.bottomAnchor.constraint(equalTo: signLabel.topAnchor, constant: 120),signLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 40), signLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -40)])
        
        NSLayoutConstraint.activate([signIn.topAnchor.constraint(equalTo: signLabel.bottomAnchor, constant: 10),signIn.leadingAnchor.constraint(equalTo: signLabel.leadingAnchor, constant: 30), signIn.trailingAnchor.constraint(equalTo: signLabel.trailingAnchor, constant: -40)])
        
    }
    
    @objc func LogIn() {
      GIDSignIn.sharedInstance.signIn(with: signInConfig, presenting: self) { user, error in
        guard error == nil else { return }
          
          guard error == nil else { return }
          guard user != nil else { return }

          NetworkManager.LogIn() {User in}
          
          NetworkManager.getCurrentUser() {User in
              let vc = TabBar(user: User)
              self.window?.rootViewController = vc
          }

          
          
      }
    }
}
