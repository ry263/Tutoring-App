//
//  CourseController.swift
//  HackChallenge2022
//
//  Created by Joel Valerio on 5/3/22.
//

import Foundation
import UIKit

class CourseController: UIViewController {
    
    weak var parentController: ProfileController?
    weak var user: User!
    let cellID = "CellID"
    var extraText = UITextView()
    var index: Int = 0
    var courses : [Course] = []
    
    
    var searchController: UISearchController!
    private var resultsTableController: ResultsTableController!
    
    convenience init(num: Int, user: User) {
        self.init()
        self.index = num
        self.user = user
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        
        view.clipsToBounds = true
        
        navigationItem.titleView?.backgroundColor = .clear
        
        if index == 1 {
            extraText.text = "Search for Cornell Courses to tutor in!"
        } else {
            extraText.text = "Search for Cornell Courses to get help in"
        }
        
        let centerY = self.view.center.y - 52.75
        let centerX = self.view.center.x - 65
        
        NetworkManager.getAllCourses() { courses in
            self.courses = courses
        }
        
        extraText.frame = CGRect(x: centerX, y: centerY, width: 130, height: 105.5)
        extraText.textAlignment = .center
        extraText.isUserInteractionEnabled = false
        extraText.font = .systemFont(ofSize: 16)
        extraText.translatesAutoresizingMaskIntoConstraints = false
        extraText.clipsToBounds = true
        view.addSubview(extraText)
        
        resultsTableController = ResultsTableController()
        resultsTableController.parentController = self
        resultsTableController.tableView.rowHeight = 40.0
        resultsTableController.tableView.delegate = self
        
        searchController = UISearchController(searchResultsController: resultsTableController)
        searchController.delegate = self
        searchController.searchBar.autocapitalizationType = .allCharacters
        searchController.searchBar.delegate = self
        searchController.searchBar.translatesAutoresizingMaskIntoConstraints = false
        searchController.searchBar.clipsToBounds = true
        view.addSubview(searchController.searchBar)
        
        definesPresentationContext = true
        
        setUpContraints()
    }
    func setUpContraints() {
        let padding = 20.0
        
        NSLayoutConstraint.activate([ searchController.searchBar.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor,constant: 2*padding),searchController.searchBar.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor,constant: -padding), searchController.searchBar.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor,constant: 10),searchController.searchBar.bottomAnchor.constraint(equalTo: searchController.searchBar.topAnchor, constant: 2 * padding)])
        
    }
    
    func showAlert() {
        let alert = UIAlertController(title: "Invalid Selection", message: "Course already added", preferredStyle: .alert)

        alert.addAction(UIAlertAction(title: "Ok", style: .cancel) {_ in })
        
        present(alert, animated: true,completion: nil)
    }
    
    func showFailure() {
        let alert = UIAlertController(title: "No course found", message: "Try Another", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "Ok", style: .cancel))
        present(alert,animated: true,completion: nil)
    }
}

// MARK: Networking Request

extension CourseController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let selectedRow = courses[indexPath.row]
        print(selectedRow.code)
        if index == 1 {
            let checkIn: Bool = parentController!.courses.contains(selectedRow)
            if  !checkIn {
                let courseID = String(selectedRow.id)
                let userID = String(user.id)
                
                NetworkManager.addTutor(courseID: courseID, userID: userID) { _ in}
                self.navigationController?.popViewController(animated: true)
                self.parentController!.courses.insert(selectedRow, at: 0)
                self.parentController?.tutoring.reloadData()
                
            } else {
                showAlert()
            }
        } else {
            let vc = TutorController(course: selectedRow)
            vc.userViewing = parentController?.userViewing
            present(vc, animated: true, completion: nil)
        }
    }
}

extension CourseController: UISearchControllerDelegate, UISearchBarDelegate {
    
    func didPresentSearchController(_ searchController: UISearchController) {
        let padding = 20.0
        
        NSLayoutConstraint.activate([ searchController.searchBar.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor,constant: 2*padding),searchController.searchBar.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding), searchController.searchBar.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 10),searchController.searchBar.bottomAnchor.constraint(equalTo: searchController.searchBar.topAnchor, constant: 2 * padding)])
        
    }
    
    
    func searchBarSearchButtonClicked(_ searchBar: UISearchBar) {
        
        if let text = searchController.searchBar.text {
            let whitespaceCharacterSet = CharacterSet.whitespaces
            let trimText = text.trimmingCharacters(in: whitespaceCharacterSet)
            let modText = trimText.replacingOccurrences(of: " ", with: "")
            
            NetworkManager.getCourse(courseCode: modText) { course in
                self.courses = [course]
                self.resultsTableController.course = [course]
                self.resultsTableController.tableView.reloadData()
            }
        }
        
        searchBar.resignFirstResponder()
    }
    
}


class ResultsTableController: UITableViewController {
    let cellReuse = "CellReuse"
    var course: [Course] = []
    weak var parentController: CourseController?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.course = parentController?.courses ?? []
        
        
        tableView.register(SearchCell.self, forCellReuseIdentifier: cellReuse)
        
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.course.count
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if let cell = tableView.dequeueReusableCell(withIdentifier: cellReuse, for: indexPath) as? SearchCell {
            
            let courses = course[indexPath.row].code
            cell.configure(course: courses)
            cell.selectionStyle = .none
            return cell
        }
        return UITableViewCell()
    }
    
    override func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 40.0
    }
}

