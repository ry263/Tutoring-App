//
//  TutorController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/4/22.
//

import Foundation
import UIKit

class TutorController: UIViewController {
    
    weak var selectedCourse: Course!
    weak var userViewing: User!
    var tutorCollection = UITableView()
    let reuse = "reuse"
    let courseTitle = UILabel()
    var displayedTutors : [User] = []
    let tutorSpacing = 35.0
    
    convenience init(course: Course) {
        self.init()
        self.selectedCourse = course
        
        self.courseTitle.text = course.code
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.view.backgroundColor = .white
        
        let modText = selectedCourse.code.replacingOccurrences(of: " ", with: "")
        NetworkManager.getTutors(courseCode: modText) { users in
            self.displayedTutors = users
        }
        
        
        self.courseTitle.font = .systemFont(ofSize: 24, weight: .bold)
        self.courseTitle.textAlignment = .center
        self.courseTitle.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(self.courseTitle)
        
        self.tutorCollection.delegate = self
        self.tutorCollection.dataSource = self
        self.tutorCollection.register(TutorCell.self, forCellReuseIdentifier: reuse)
        self.tutorCollection.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(self.tutorCollection)
        
        setUpConstraints()
    }
    
    func setUpConstraints() {
        
        NSLayoutConstraint.activate([courseTitle.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 20),courseTitle.bottomAnchor.constraint(equalTo: courseTitle.topAnchor, constant: 20), courseTitle.leadingAnchor.constraint(equalTo: view.centerXAnchor, constant: -80), courseTitle.trailingAnchor.constraint(equalTo: view.centerXAnchor, constant: 80)])
        
        NSLayoutConstraint.activate([tutorCollection.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20), tutorCollection.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20), tutorCollection.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 40), tutorCollection.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: 20)])
    }
    
    override func viewDidAppear(_ animated: Bool) {
        tutorCollection.reloadData()
    }
    
}

extension TutorController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        let selectedTutor = displayedTutors[indexPath.row]
        let vc = ProfileController(ownAccount: false, user: selectedTutor)
        vc.userViewing = userViewing
        vc.addTime = Availability(time: "+ Add a new time!", userID: userViewing.id, ID: 1000000)
        present(vc, animated: true, completion: nil)
    }
}
extension TutorController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        self.displayedTutors.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        print(self.displayedTutors.count)
        if let cell = tableView.dequeueReusableCell(withIdentifier: reuse, for: indexPath) as? TutorCell {
            let tutor = self.displayedTutors[indexPath.row]
            cell.configure(user: tutor)
            return cell
        }
        return UITableViewCell()
    }
}
    
    
