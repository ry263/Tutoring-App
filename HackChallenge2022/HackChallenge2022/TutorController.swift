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
    let flowLayout = UICollectionViewFlowLayout()
    var tutorCollection = UICollectionView(frame: .zero, collectionViewLayout: UICollectionViewLayout())
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
        
        view.backgroundColor = .white
        
        selectedCourse.tutors.append(Josh)
        selectedCourse.tutors.append(Joel)
        selectedCourse.tutors.append(Lukman)
        displayedTutors = getTutors(course: selectedCourse)
        
        courseTitle.font = .systemFont(ofSize: 24, weight: .bold)
        courseTitle.textAlignment = .center
        courseTitle.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(courseTitle)
        
        flowLayout.scrollDirection = .vertical
        flowLayout.minimumLineSpacing = tutorSpacing
        flowLayout.minimumInteritemSpacing = tutorSpacing
        
        tutorCollection = UICollectionView(frame: .zero, collectionViewLayout: flowLayout)
        tutorCollection.delegate = self
        tutorCollection.dataSource = self
        tutorCollection.translatesAutoresizingMaskIntoConstraints = false
        tutorCollection.register(TutorCell.self, forCellWithReuseIdentifier: reuse)
        view.addSubview(tutorCollection)
        
        setUpConstraints()
    }
    
    func getTutors(course: Course) -> [User] {
        return course.tutors
    }
    
    func setUpConstraints() {
        
        NSLayoutConstraint.activate([courseTitle.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 20),courseTitle.bottomAnchor.constraint(equalTo: courseTitle.topAnchor, constant: 20), courseTitle.leadingAnchor.constraint(equalTo: view.centerXAnchor, constant: -80), courseTitle.trailingAnchor.constraint(equalTo: view.centerXAnchor, constant: 80)])
        
        NSLayoutConstraint.activate([tutorCollection.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20), tutorCollection.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20), tutorCollection.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 40), tutorCollection.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: 20)])
    }
    
}

// TODO: Load selected tutor information from backend
extension TutorController: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let selectedTutor = displayedTutors[indexPath.row]
        let vc = ProfileController(ownAccount: false, user: selectedTutor)
        // Send getUserbyID request
        vc.userViewing = userViewing
        vc.addTime = Availability(time: "+ Add a new time!", userID: userViewing.id, ID: 1000000)
        present(vc, animated: true, completion: nil)
        
        
    }
}
// TODO: Load tutors from backend
extension TutorController: UICollectionViewDataSource, UICollectionViewDelegateFlowLayout {
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
            let padding: CGFloat =  50
            let collectionViewSize = collectionView.frame.size.width - padding
            
            return CGSize(width: collectionViewSize/2, height: collectionViewSize/2)
        }
    
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return displayedTutors.count/2
    }


    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return displayedTutors.count
    }

    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        if let cell = collectionView.dequeueReusableCell(withReuseIdentifier: reuse, for: indexPath) as? TutorCell {
            let tutor = displayedTutors[indexPath.row]
            cell.configure(userPic: tutor.profile_pic)
            return cell
        }
        return UICollectionViewCell()
    }
    
}
    
